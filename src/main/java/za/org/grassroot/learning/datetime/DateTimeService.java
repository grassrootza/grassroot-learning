package za.org.grassroot.learning.datetime;

import edu.stanford.nlp.ie.AbstractSequenceClassifier;
import edu.stanford.nlp.pipeline.AnnotationPipeline;
import edu.stanford.nlp.time.SUTime;

import java.time.LocalDateTime;

/**
 * Created by shakka on 8/15/16.
 */
public interface DateTimeService {

    LocalDateTime parse(String phrase);

    String getNerParse(AbstractSequenceClassifier ner, String phrase);

    LocalDateTime getSUTimeParse(AnnotationPipeline pipeline, String edited);

    LocalDateTime temporalToLocalDateTime(SUTime.Temporal temporal);

}
