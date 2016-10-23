package za.org.grassroot.learning.worddist;

import java.util.Map;

/**
 * Created by luke on 2016/10/16.
 */
public interface DistanceMeasurer {

    void calculateDistances(String searchTerm);

	Map<String, Double> calculateDistances(String searchTerm, int N);

    Map<String, Double> findTermsWithinDistance(String searchTerm, double minDistance);
}
