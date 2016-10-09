package za.org.grassroot.learning.worddist;

import org.apache.commons.math3.linear.ArrayRealVector;
import org.apache.commons.math3.linear.RealVector;
import org.ejml.simple.SimpleMatrix;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;

/**
 * Created by luke on 2016/10/03.
 */
public class DistanceMeasurer {

    private static final Logger logger = LoggerFactory.getLogger(DistanceMeasurer.class);

    public void readInVector() {
        try {
            SimpleMatrix simpleMatrix = SimpleMatrix.loadCSV("csvFile.txt"); // todo : read this location from properties file
            RealVector apacheCommonsRealVector = new ArrayRealVector();
        } catch (IOException e) {
            logger.info("Error loading matrix from file!");
            e.printStackTrace();
        }
    }

}
