package za.org.grassroot.learning.datetime;

import java.time.LocalDate;
import java.time.LocalTime;
import java.time.Year;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
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
import org.springframework.stereotype.Service;


/**
 * Created by shakka on 7/28/16.
 */

@Service
public class DateTimeServiceImpl implements DateTimeService {

    private static final int currentYear = Year.now().getValue() % 1000;
    private static final int nextYear = Year.now().getValue() % 1000 + 1;

    private static final Logger log = LoggerFactory.getLogger(DateTimeServiceImpl.class);

    private AnnotationPipeline pipeline;
    private AbstractSequenceClassifier ner;


    public DateTimeServiceImpl() {
        initPipelineAndNER();
    }

    public LocalDateTime parse(String phrase) {
        long start = System.currentTimeMillis();
        String edited = getNerParse(ner, phrase.toLowerCase());
        log.info("Time to get NER parse: {}", System.currentTimeMillis() - start);

        start = System.currentTimeMillis();
        LocalDateTime parsedDateTime = getSUTimeParse(pipeline, edited);
        log.info("Time to get parsed LDT: {}", System.currentTimeMillis() - start);
        return parsedDateTime;
    }

    public String getNerParse(AbstractSequenceClassifier ner, String original) {
        original = original.toLowerCase();
        // Case: date with time not explicitly stated, e.g. 01/07/16 11:30
        original = original.replace("/" + currentYear + " ", "/20" + currentYear + " ");
        original = original.replace("/" + nextYear + " ", "/20" + nextYear + " ");

        // Case: Date and time are one token e.g. tomorrow@5
        original = original.replaceAll("@", " @ ");

        List<Triple<String, Integer, Integer>> entities = ner.classifyToCharacterOffsets(original);
        String edited = original;

        for (int i = entities.size() - 1; i > -1; i--) {
            Triple t = entities.get(i);
            edited = edited.replace(edited.substring((Integer)t.second(),(Integer)t.third()), t.first().toString());
        }

        return edited;
    }

    public LocalDateTime getSUTimeParse(AnnotationPipeline pipeline, String edited) {
        edited = edited.toLowerCase();
        Annotation annotation = new Annotation(edited);
        annotation.set(CoreAnnotations.DocDateAnnotation.class, LocalDateTime.now().toString());
        pipeline.annotate(annotation);
        List<CoreMap> timexAnnsAll = annotation.get(TimeAnnotations.TimexAnnotations.class);
        LocalDateTime parse;

        if (timexAnnsAll.size() > 1) {
            List<LocalDateTime> dt = new ArrayList<>();
            for (CoreMap cm : timexAnnsAll) {
                List<CoreLabel> tokens = cm.get(CoreAnnotations.TokensAnnotation.class);

                SUTime.Temporal temporal = cm.get(TimeExpression.Annotation.class).getTemporal();
                LocalDateTime dateTime = temporalToLocalDateTime(temporal);
                dt.add(dateTime);
            }
            //assumes user enters date and then time
            LocalDate date = dt.get(0).toLocalDate();
            LocalTime time = dt.get(1).toLocalTime();
            parse = LocalDateTime.of(date, time);

        } else {
            try {
                CoreMap cm = timexAnnsAll.get(0);

                List<CoreLabel> tokens = cm.get(CoreAnnotations.TokensAnnotation.class);

                SUTime.Temporal temporal = cm.get(TimeExpression.Annotation.class).getTemporal();

                parse = temporalToLocalDateTime(temporal);
            } catch (IndexOutOfBoundsException e) {
                parse = LocalDateTime.now();
            }
        }

        return parse;
    }

    private void initPipelineAndNER(){
        Properties props = new Properties();
        this.pipeline = new AnnotationPipeline();
        pipeline.addAnnotator(new TokenizerAnnotator(false));
        pipeline.addAnnotator(new WordsToSentencesAnnotator(false));
        pipeline.addAnnotator(new POSTaggerAnnotator(false));
        pipeline.addAnnotator(new TimeAnnotator("sutime", props));

        String serializedClassifier = "../grassroot-resources/classifiers/ner-model-datetime.ser.gz";

        this.ner = CRFClassifier.getClassifierNoExceptions(serializedClassifier);
    }

    public LocalDateTime temporalToLocalDateTime(SUTime.Temporal temporal) {
        String iso = temporal.toISOString();

        DateTimeFormatter formatter = DateTimeFormatter.ISO_LOCAL_DATE_TIME;
        if (!temporal.getTime().hasTime()) {
            iso = temporal.toISOString() + "T" + LocalTime.now().toString().substring(0, 5);
        }
        LocalDateTime dateTime;

        try {
            dateTime = LocalDateTime.parse(iso, formatter);
        } catch (DateTimeParseException e) {
            dateTime = LocalDateTime.now();
        }

        if ( (dateTime.toLocalDate().compareTo(LocalDateTime.now().toLocalDate()) < 0)
                && (dateTime.compareTo(LocalDateTime.now().minusWeeks(1)) > 0))
            dateTime = dateTime.plusWeeks(1);

        return dateTime;
    }
}
