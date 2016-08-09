package za.org.grassroot.learning;


import org.joda.time.DateTime;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.*;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.NestedServletException;
import org.springframework.web.util.UriComponentsBuilder;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.net.URI;
import java.net.URL;
import java.net.URLEncoder;
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

    @RequestMapping(value = "/", method = RequestMethod.GET)
    public String compare(Model model) {
        DateTimeService selo = new DateTimeService();
        model.addAttribute("selo", selo);

        return "compare";
    }

    @RequestMapping(value = "/results", method = RequestMethod.POST)
    public String datetimeService(@ModelAttribute(value="selo") DateTimeService selo, Model model) throws Exception {

        log.info("Original string: {}", selo.getUnparsed());
        model.addAttribute("originalPhrase", selo.getUnparsed());
        model.addAttribute("seloParse", selo.parseDatetime());
        log.info("Selo parse: {}", selo.parseDatetime());

        RestTemplate restTemplate = new RestTemplate();

        String url = "https://staging.grassroot.org.za/api/language/test/natty?inputString=" + selo.getUnparsed();

        try {
            NattyValue nattyValue = restTemplate.getForObject(url, NattyValue.class);
            String nattyJson = restTemplate.getForObject(url, String.class);

            NattyData nattyData = nattyValue.getData();
            log.info("Natty JSON = " + nattyJson);

            LocalDateTime natty = LocalDateTime.of(nattyData.getYear(), nattyData.getMonthValue(), nattyData.getDayOfMonth(),
                    nattyData.getHour(), nattyData.getMinute());

            model.addAttribute("nattyParse", natty.toString());
            log.info("NattyData monthValue: {}", nattyData.getMonthValue());
            log.info("NattyData year: {}", nattyData.getYear());
            log.info("NattyData dayOfMonth: {}", nattyData.getDayOfMonth());

            log.info("NattyData: {}", nattyData.toString());

            log.info("Natty URL: {}", url);
            log.info("Natty parse: {}", natty.toString());
        } catch (RestClientException e) {
            log.info("Natty unable to parse");
        }

        //compareNattySeloResults("/home/shakka/Projects/Grassroot/grassroot-learning/src/main/resources/extracted_dates.txt");
        return "results";
    }


    public void compareNattySeloResults(String filename) throws IOException{

        log.info("Putting results from Natty into file...");

        ArrayList<String> datetimes = new ArrayList<String>();
        datetimes.add("Original \t | Selo \t | Natty");
        RestTemplate restTemplate = new RestTemplate();
        DateTimeService selo = new DateTimeService();

        try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = br.readLine()) != null) {

                log.info("line: {}", line);
                selo.setUnparsed(line);
                log.info("Selo parse: {}", selo.parseDatetime());
                String compare = line;

                compare = compare + "\t |" + selo.parseDatetime();

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

        Path file  = Paths.get("selo-natty-results2.txt");
        Files.write(file, datetimes, Charset.forName("UTF-8"));

    }
}
