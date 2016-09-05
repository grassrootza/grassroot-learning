package za.org.grassroot.learning;


import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;
import za.org.grassroot.learning.datetime.DateTimeService;
import za.org.grassroot.learning.datetime.SeloParseException;

import java.time.LocalDateTime;

/**
 * Created by shakka on 7/29/16.
 */
@Controller
public class DatetimeController {

    private static final Logger log = LoggerFactory.getLogger(DatetimeController.class);

    @Autowired
    private DateTimeService selo;

    @RequestMapping(value="/parse", method = RequestMethod.GET)
    public @ResponseBody String dateTime(@RequestParam(value="phrase", defaultValue = "") String phrase) {
        log.info("String to be parsed: {}", phrase);
        try {
            return selo.parse(phrase).toString();
        } catch (SeloParseException e) {
            log.info("Error with {}", phrase);
            return "ERROR_PARSING";
        }
    }

    @RequestMapping(value = "/compare", method = RequestMethod.GET)
    public String compare(Model model) {
        return "compare";
    }

    @RequestMapping(value = "/results", method = RequestMethod.POST)
    public String datetimeService(@RequestParam("phrase") String phrase, Model model) throws Exception {

        log.info("Original string: {}", phrase);
        model.addAttribute("originalPhrase", phrase);

        String seloParse = selo.parse(phrase).toString();
        model.addAttribute("seloParse", seloParse);
        log.info("Selo parse: {}", seloParse);

        RestTemplate restTemplate = new RestTemplate();

        String url = "https://staging.grassroot.org.za/api/language/test/natty?inputString=" + phrase;

        try {
            NattyValue nattyValue = restTemplate.getForObject(url, NattyValue.class);

            NattyData nattyData = nattyValue.getData();

            LocalDateTime natty = LocalDateTime.of(nattyData.getYear(), nattyData.getMonthValue(), nattyData.getDayOfMonth(),
                    nattyData.getHour(), nattyData.getMinute());

            model.addAttribute("nattyParse", natty.toString());
            log.info("Natty parse: {}", natty.toString());
        } catch (RestClientException e) {
            log.info("Natty unable to parse");
        }

        return "results";
    }

}
