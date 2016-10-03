package za.org.grassroot.learning.worddist;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.annotation.PostConstruct;

/**
 * Created by luke on 2016/10/03.
 */
@Controller
public class WordDistController {

    private DistanceMeasurer distanceMeasurer;

    @PostConstruct
    public void init() {
        distanceMeasurer = new DistanceMeasurer();
        distanceMeasurer.readInVector();
    }

    @RequestMapping(value = "/similar_terms", method = RequestMethod.GET)
    public @ResponseBody String similarTerms(@RequestParam String term, @RequestParam double cosineDistanceLimit) {
        // to do : return all terms within the given cosine distance
        return "tbd";
    }

}
