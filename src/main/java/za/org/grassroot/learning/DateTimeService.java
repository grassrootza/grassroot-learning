package za.org.grassroot.learning;

import java.io.InputStreamReader;
import java.net.URL;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;
import java.util.Properties;
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


/**
 * Created by shakka on 7/28/16.
 */
public class DateTimeService {

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
        for (CoreMap cm : timexAnnsAll) {
            List<CoreLabel> tokens = cm.get(CoreAnnotations.TokensAnnotation.class);

            //TODO 2 tokens -> need to concatenate into 1
            //TODO return LocalDateTime object
            //Calendar calendar = cm.get(TimeAnnotations.TimexAnnotation.class).getDate();
            // look at LocalDateTime adjustInto(Temporal temporal)
            // LocalDateTime withHour, withMinute
            return cm.get(TimeExpression.Annotation.class).getTemporal().toString();
        }
        return "";
    }

    private static void readFromFile(AnnotationPipeline pipeline, AbstractSequenceClassifier ner, String filename) throws IOException{

        ArrayList<String> datetimes = new ArrayList<String>();

        try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = br.readLine()) != null) {
                String sutime = getSUTimeStr(pipeline, getEditedStr(ner, line));
                datetimes.add(line + " | " + sutime);
            }
        }

        Path file  = Paths.get("datetime-results.txt");
        Files.write(file, datetimes, Charset.forName("UTF-8"));
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
}
