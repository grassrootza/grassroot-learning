package za.org.grassroot.learning.datetime;

import java.time.LocalDate;
import java.time.LocalTime;
import java.time.Year;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.time.LocalDateTime;

import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.time.*;
import edu.stanford.nlp.util.CoreMap;
import edu.stanford.nlp.ie.crf.*;
import edu.stanford.nlp.ie.AbstractSequenceClassifier;
import edu.stanford.nlp.util.Triple;
import org.apache.tomcat.jni.Local;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Service;

import javax.annotation.PostConstruct;


/**
 * Created by shakka on 7/28/16.
 */

@Service
public class DateTimeServiceImpl implements DateTimeService {

    private static final Logger log = LoggerFactory.getLogger(DateTimeServiceImpl.class);

    private static final int currentYear = Year.now().getValue() % 1000;
    private static final int nextYear = Year.now().getValue() % 1000 + 1;
    private static final String NOW = "PRESENT_REF";

    @Autowired
    Environment environment;

    private AnnotationPipeline pipeline;
    private AbstractSequenceClassifier ner;

    @PostConstruct
    public void initPipelineAndNER() {
        this.pipeline = new AnnotationPipeline();
        pipeline.addAnnotator(new TokenizerAnnotator(false));
        pipeline.addAnnotator(new WordsToSentencesAnnotator(false));
        pipeline.addAnnotator(new POSTaggerAnnotator(false));
        pipeline.addAnnotator(new TimeAnnotator("sutime", new Properties()));

        final String serializedClassifier = environment.getRequiredProperty("classifier.datetime.grassroot.path");
        this.ner = CRFClassifier.getClassifierNoExceptions(serializedClassifier);
    }

    public LocalDateTime parse(String phrase) {
        Objects.requireNonNull(phrase);

        try {
            long start = System.currentTimeMillis();
            final String edited = getNerParse(ner, phrase);
            log.info("Time to get NER parse: {} msecs", System.currentTimeMillis() - start);

            start = System.currentTimeMillis();
            LocalDateTime parsedDateTime = getSUTimeParse(pipeline, edited);
            log.info("Time to get parsed LDT: {} msecs", System.currentTimeMillis() - start);
            return parsedDateTime;
        } catch (Exception e) {
            throw new SeloParseException();
        }
    }

    /**
     * Created by shakka on 7/28/16.
     *
     * Pre-processes the passed string before it is fed into SUTime. Pre-processing includes toLowerCase(), which helps
     * selo parse it, and replace methods to make the string fit into established SUTime parse cases. After pre-processing,
     * selo parses the string, removing any misspelled days of week or months and replacing them with correctly spelled
     * variants.
     *
     * @param ner selo  Used to replace misspelled days of week or months with the correctly spelled version
     * @param passedString  The string to be parsed by selo
     * @return  an edited version of passedString with correctly spelled days of week and months
     */
    public String getNerParse(AbstractSequenceClassifier ner, String passedString) {
        String original = passedString.toLowerCase();

        // Case: date with time not explicitly stated, e.g. 01/07/16 11:30
        original = original.replace("/" + currentYear + " ", "/20" + currentYear + " ");
        original = original.replace("/" + nextYear + " ", "/20" + nextYear + " ");

        // Case: Date and time are one token e.g. tomorrow@5
        original = original.replaceAll("@", " @ ");

        List<Triple<String, Integer, Integer>> entities = ner.classifyToCharacterOffsets(original);
        String edited = original;

        // replace misspelled word in original string with correctly spelled version
        for (int i = entities.size() - 1; i > -1; i--) {
            Triple t = entities.get(i);
            edited = edited.replace(edited.substring((Integer)t.second(),(Integer)t.third()), t.first().toString());
        }

        return edited;
    }

    /**
     * Created by shakka on 7/28/16.
     *
     * Uses a custom-build version of Stanford's SUTime to parse the editedInputString into a SUTime Temporal object
     * This temporal is fed into another function that converts it into a LocalDateTime.
     *
     * @param pipeline  Used to feed the string into SUTime
     * @param editedInputString  The string to be passed into SUTime, previously parsed by selo
     * @return  a LocalDateTime based on the editedInputString
     */
    public LocalDateTime getSUTimeParse(AnnotationPipeline pipeline, String editedInputString) {
        Annotation annotation = new Annotation(editedInputString);
        annotation.set(CoreAnnotations.DocDateAnnotation.class, LocalDateTime.now().toString());
        pipeline.annotate(annotation);
        List<CoreMap> timexAnnsAll = annotation.get(TimeAnnotations.TimexAnnotations.class);
        LocalDateTime parseResult;

        if (timexAnnsAll.size() > 1) {
            List<LocalDateTime> separateDateAndTime = new ArrayList<>();
            for (CoreMap cm : timexAnnsAll) {
                SUTime.Temporal temporal = cm.get(TimeExpression.Annotation.class).getTemporal();
                separateDateAndTime.add(temporalToLocalDateTime(temporal));
            }
            //assumes user enters full date and then time e.g. 9 July 2016 4pm // todo : refine to handle reverse order
            LocalDate date = separateDateAndTime.get(0).toLocalDate();
            LocalTime time = separateDateAndTime.get(1).toLocalTime();
            parseResult = LocalDateTime.of(date, time);
        } else if (!timexAnnsAll.isEmpty()){
            CoreMap cm = timexAnnsAll.get(0);
            List<CoreLabel> tokens = cm.get(CoreAnnotations.TokensAnnotation.class);
            SUTime.Temporal temporal = cm.get(TimeExpression.Annotation.class).getTemporal();
            parseResult = temporalToLocalDateTime(temporal);
        } else {
            throw new SeloParseException();
        }

        return parseResult;
    }

    public LocalDateTime temporalToLocalDateTime(SUTime.Temporal temporal) {
        String iso = temporal.toISOString();
        LocalDateTime dateTime;

        DateTimeFormatter formatter = DateTimeFormatter.ISO_LOCAL_DATE_TIME;

        if (temporal.toString().equals(NOW)) {
            dateTime = LocalDateTime.now().truncatedTo(ChronoUnit.MINUTES);
        } else if (!temporal.getTime().hasTime()) {
            DateTimeFormatter dateFormatter = DateTimeFormatter.ISO_DATE;
            dateTime = LocalDateTime.of(LocalDate.parse(iso, dateFormatter), LocalTime.now().truncatedTo(ChronoUnit.MINUTES));
            //iso = temporal.toISOString() + "T" + LocalTime.now().toString().substring(0, 5);
        } else {

            try {
                dateTime = LocalDateTime.parse(iso, formatter);
            } catch (DateTimeParseException e) {
                throw new SeloParseException();
            }

            if ((dateTime.toLocalDate().compareTo(LocalDateTime.now().toLocalDate()) < 0)
                    && (dateTime.compareTo(LocalDateTime.now().minusWeeks(1)) > 0))
                dateTime = dateTime.plusWeeks(1);
        }

        return dateTime;
    }
}
