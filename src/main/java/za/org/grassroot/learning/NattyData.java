package za.org.grassroot.learning;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

/**
 * Created by shakka on 8/8/16.
 */
@JsonIgnoreProperties(ignoreUnknown = true)
public class NattyData {

    private int monthValue;
    private int hour;
    private int minute;
    private int year;
    private String month;
    private int dayOfMonth;

    public NattyData() {
    }

    public int getMonthValue() {
        return monthValue;
    }

    public void setMonthValue(int monthValue) {
        this.monthValue = monthValue;
    }

    public int getHour() {
        return hour;
    }

    public void setHour(int hour) {
        this.hour = hour;
    }

    public int getMinute() {
        return minute;
    }

    public void setMinute(int minute) {
        this.minute = minute;
    }

    public int getYear() {
        return year;
    }

    public void setYear(int year) {
        this.year = year;
    }

    public String getMonth() {
        return month;
    }

    public void setMonth(String month) {
        this.month = month;
    }

    public int getDayOfMonth() {
        return dayOfMonth;
    }

    public void setDayOfMonth(int dayOfMonth) {
        this.dayOfMonth = dayOfMonth;
    }
}
