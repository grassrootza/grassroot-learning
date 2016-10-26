package za.org.grassroot.learning.worddist;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.Map;

/**
 * Created by luke on 2016/10/03.
 */
@Controller
public class WordDistController {

    private static final Logger logger = LoggerFactory.getLogger(WordDistController.class);

    private static final double DEFAULT_MIN_DISTANCE = 0.5;

    private final DistanceMeasurer distanceMeasurer;

    @Autowired
    public WordDistController(DistanceMeasurer distanceMeasurer) {
        this.distanceMeasurer = distanceMeasurer;
    }

    @RequestMapping(value = "/related", method = RequestMethod.GET)
    public @ResponseBody
    Map<String, Double> similarTerms(@RequestParam String term, @RequestParam(value = "minDist", required = false) Double cosineDistanceLimit) {
        logger.info("Looking up distances for term: " + term);
        return distanceMeasurer.findTermsWithinDistance(term.toLowerCase(), cosineDistanceLimit == null ? DEFAULT_MIN_DISTANCE : cosineDistanceLimit);
    }

}
