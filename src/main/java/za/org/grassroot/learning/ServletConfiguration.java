package za.org.grassroot.learning;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.filter.CharacterEncodingFilter;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurerAdapter;

import javax.servlet.Filter;

/**
 * Created by luke on 2016/08/20.
 * todo : wire up properly (also add path restrictions, static pages, and the like)
 */
@Configuration
@ControllerAdvice
public class ServletConfiguration extends WebMvcConfigurerAdapter {

    // todo : insert java 8 date time dialect

    @Bean
    public Filter characterEncodingFilter() {
        CharacterEncodingFilter filter = new CharacterEncodingFilter();
        filter.setEncoding("UTF-8");
        filter.setForceEncoding(true);
        return filter;
    }

}
