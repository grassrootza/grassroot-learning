package za.org.grassroot.learning.datetime;


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
import za.org.grassroot.learning.NattyData;
import za.org.grassroot.learning.NattyValue;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.util.ArrayList;

/**
 * Created by shakka on 7/29/16.
 */
@Controller
public class DatetimeController {

    private static final Logger log = LoggerFactory.getLogger(DatetimeController.class);

    @Autowired
    private DateTimeServiceImpl selo;


    @RequestMapping(value="/parse", method = RequestMethod.GET)
    public @ResponseBody String dateTime(@RequestParam(value="phrase", defaultValue = "") String phrase) {
        log.info("String to be parsed: {}", phrase);
        return selo.parse(phrase).toString();
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
            String nattyJson = restTemplate.getForObject(url, String.class);

            NattyData nattyData = nattyValue.getData();

            LocalDateTime natty = LocalDateTime.of(nattyData.getYear(), nattyData.getMonthValue(), nattyData.getDayOfMonth(),
                    nattyData.getHour(), nattyData.getMinute());

            model.addAttribute("nattyParse", natty.toString());
            log.info("Natty parse: {}", natty.toString());
        } catch (RestClientException e) {
            log.info("Natty unable to parse");
        }

        //compareNattySeloResults("/home/shakka/Projects/Grassroot/grassroot-learning/src/main/resources/aug14_extracted_dates.txt");
        return "results";
    }


    public void compareNattySeloResults(String filename) throws IOException{

        log.info("Putting results from Natty into file...");

        ArrayList<String> datetimes = new ArrayList<String>();
        datetimes.add("Original \t | Selo \t | Natty");
        RestTemplate restTemplate = new RestTemplate();
        DateTimeServiceImpl selo = new DateTimeServiceImpl();

        try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = br.readLine()) != null) {

                log.info("line: {}", line);
                log.info("Selo parse: {}", selo.parse(line).toString());
                String compare = line;

                compare = compare + "\t |" + selo.parse(line).toString();

                String url = "https://staging.grassroot.org.za/api/language/test/natty?inputString=" + line;

                try {
                    NattyValue nattyValue = restTemplate.getForObject(url, NattyValue.class);
                    NattyData nattyData = nattyValue.getData();

                    LocalDateTime natty = LocalDateTime.of(nattyData.getYear(), nattyData.getMonthValue(), nattyData.getDayOfMonth(),
                            nattyData.getHour(), nattyData.getMinute());

                    log.info("Natty parse: {}\n", natty.toString());
                    compare = compare + "\t | " + natty.toString();

                } catch (RestClientException e) {
                    log.info("Natty unable to parse \n");
                }

             datetimes.add(compare);
            }
        }

        Path file  = Paths.get("selo-natty-results-aug14.txt");
        Files.write(file, datetimes, Charset.forName("UTF-8"));

    }
}
