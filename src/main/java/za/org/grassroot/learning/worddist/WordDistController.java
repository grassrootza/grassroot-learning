package za.org.grassroot.learning.worddist;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

/**
 * Created by luke on 2016/10/03.
 */
@Controller
@RequestMapping("/word_dist/")
public class WordDistController {

    private static final Logger logger = LoggerFactory.getLogger(WordDistController.class);

    @Autowired
    private DistanceMeasurer distanceMeasurer;

    @RequestMapping(value = "/similar_terms", method = RequestMethod.GET)
    public @ResponseBody String similarTerms(@RequestParam String term, @RequestParam(required = false) Double cosineDistanceLimit) {
        // to do : return all terms within the given cosine distance
        logger.info("Looking up distances for term: " + term);
        distanceMeasurer.calculateDistances(term.toLowerCase());
        return "tbd";
    }

}
