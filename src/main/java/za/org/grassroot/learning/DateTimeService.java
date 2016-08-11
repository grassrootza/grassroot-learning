package za.org.grassroot.learning;

import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.*;
import java.time.LocalDateTime;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.FileReader;

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


/**
 * Created by shakka on 7/28/16.
 */
public class DateTimeService {

    private static final Logger log = LoggerFactory.getLogger(DateTimeService.class);

    private String unparsed;
    private String parsed;
    private AnnotationPipeline pipeline;
    private AbstractSequenceClassifier ner;

    public DateTimeService(String unparsed){

        // needs to be lower case for classifier to work properly
        this.unparsed = unparsed.toLowerCase();
        this.parsed = "";

        initPipelineAndNER();
    }

    public DateTimeService() {
        this.unparsed = "";
        this.parsed = "";

        initPipelineAndNER();
    }


    public String getUnparsed() { return unparsed; }

    public String getParsed() {return parsed; }

    public void setParsed(String p) {
        parsed = p;
    }

    public void setUnparsed(String p) {unparsed = p.toLowerCase();}


    public String parseDatetime() {

        String edited = getEditedStr(ner, unparsed);
        String sutime = getSUTimeStr(pipeline, edited);

        setParsed(sutime);

        return sutime;
    }

    private static String getEditedStr(AbstractSequenceClassifier ner, String original) {

        List<Triple<String, Integer, Integer>> entities = ner.classifyToCharacterOffsets(original);
        String edited = original;

        for (int i = entities.size() - 1; i > -1; i--) {
            Triple t = entities.get(i);
            edited = edited.replace(edited.substring((Integer)t.second(),(Integer)t.third()), t.first().toString());
        }

        return edited;
    }

    private static String getSUTimeStr(AnnotationPipeline pipeline, String edited) {
        Annotation annotation = new Annotation(edited);
        annotation.set(CoreAnnotations.DocDateAnnotation.class, LocalDateTime.now().toString());
        pipeline.annotate(annotation);
        List<CoreMap> timexAnnsAll = annotation.get(TimeAnnotations.TimexAnnotations.class);
        String parse = "";

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
            LocalDateTime combo = LocalDateTime.of(date, time);

            log.info("date: {}", date.toString());
            log.info("time: {}", time.toString());
            log.info("combo: {}", combo.toString());

            parse = combo.toString();

        } else {
            for (CoreMap cm : timexAnnsAll) {
                List<CoreLabel> tokens = cm.get(CoreAnnotations.TokensAnnotation.class);

                log.info("num tokens: {}", tokens.size());

                SUTime.Temporal temporal = cm.get(TimeExpression.Annotation.class).getTemporal();
                LocalDateTime dateTime = temporalToLocalDateTime(temporal);

                parse = dateTime.toString();
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

        String serializedClassifier = "src/main/resources/classifiers/ner-model-datetime.ser.gz";
        this.ner = CRFClassifier.getClassifierNoExceptions(serializedClassifier);
    }

    private static LocalDateTime temporalToLocalDateTime(SUTime.Temporal temporal) {
        String iso = temporal.toISOString();

        log.info("temporal str: {}", iso);
        DateTimeFormatter formatter = DateTimeFormatter.ISO_LOCAL_DATE_TIME;
        if (!temporal.getTime().hasTime()) {
            iso = temporal.toISOString() + "T" + LocalTime.now().toString().substring(0, 5);
            log.info("temporal str: {}", iso);
        }
        LocalDateTime dateTime;

        try {
            dateTime = LocalDateTime.parse(iso, formatter);
        } catch (DateTimeParseException e) {
            dateTime = LocalDateTime.now();
        }
        log.info("datetime str: {}", dateTime.toString());

        if ( (dateTime.toLocalDate().compareTo(LocalDateTime.now().toLocalDate()) < 0)
                && (dateTime.compareTo(LocalDateTime.now().minusWeeks(1)) > 0))
            dateTime = dateTime.plusWeeks(1);

        log.info("datetime str: {}", dateTime.toString());
        return dateTime;
    }
}
