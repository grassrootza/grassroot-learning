package za.org.grassroot.learning;

import java.time.LocalDateTime;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

/**
 * Created by shakka on 8/8/16.
 */
@JsonIgnoreProperties(ignoreUnknown = true)
public class NattyValue {

    private String status;
    private int code;
    private String message;
    private NattyData data;

    public NattyValue() {}

    public NattyData getData() {
        return data;
    }

    public void setData(NattyData data) {
        this.data = data;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public int getCode() {
        return code;
    }

    public void setCode(int code) {
        this.code = code;
    }
}
