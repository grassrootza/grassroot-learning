package za.org.grassroot.learning.worddist;

import org.apache.commons.math3.linear.ArrayRealVector;
import org.apache.commons.math3.linear.MatrixUtils;
import org.apache.commons.math3.linear.RealMatrix;
import org.apache.commons.math3.linear.RealVector;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.context.event.EventListener;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;
import java.util.stream.IntStream;

/**
 * Created by luke on 2016/10/03.
 */
@Service
public class DistanceMeasurerImpl implements DistanceMeasurer {

    private static final Logger logger = LoggerFactory.getLogger(DistanceMeasurerImpl.class);

	private Map<String, Integer> vocab;
	private Map<Integer, String> iVocab;
	private Set<String> universe;

	private RealMatrix W;

	private final Environment environment;

	@Autowired
	public DistanceMeasurerImpl(Environment environment) {
		this.environment = environment;
	}

	@EventListener
	public void handleApplicationStarted(ApplicationReadyEvent event) {
		logger.info("Building vectors for word distance service ...");
		vocab = new HashMap<>();
		iVocab = new HashMap<>();
		universe = new HashSet<>();
		long startTime=System.currentTimeMillis();
		W = generate(environment.getProperty("grassroot.worddist.vocab.path"),
				environment.getProperty("grassroot.worddist.vectors.path"),
				environment.getProperty("grassroot.worddist.universe.path"));
		long endTime = System.currentTimeMillis();
		logger.info("Completed word dist initialization in: {} seconds", (endTime - startTime) / 1000);
	}

	@Override
	public Map<String, Double> calculateDistances(String searchTerm, int N) {
		
		List<Double> negativeDist = new ArrayList<>();

		int[] sortedIndices = getSortedDistances(searchTerm, negativeDist);

		// assuming that a.length is what was meant by N
		Map<String, Double> matches = new LinkedHashMap<String, Double>();
		int numPrinted = 0;
		for(int i = 0; i < sortedIndices.length && numPrinted < N; i++) {
			int wordID = sortedIndices[i]; 
			String word = iVocab.get(wordID);
			Double wordDistance = negativeDist.get(wordID);
			if (!universe.contains(word)) {
				continue;
			}
			logger.info(word + " " + wordDistance);
			matches.put(word, wordDistance);
			numPrinted++;
		}
		return matches;
	}

	@Override
	public Map<String, Double> findTermsWithinDistance(String searchTerm, double minDistance) {
		if (!vocab.containsKey(searchTerm)) {
			logger.info("Word not contained in vocab");
			return new HashMap<>();
		} else {
			Objects.requireNonNull(searchTerm);

			List<Double> negativeDist = new ArrayList<>();
			int[] sortedIndices = getSortedDistances(searchTerm, negativeDist);
			logger.info("Found {} words within distance", sortedIndices.length);

			Map<String, Double> matches = new LinkedHashMap<>();
			for (int wordID : sortedIndices) {
				String word = iVocab.get(wordID);
				Double wordDistance = negativeDist.get(wordID);
				if (wordDistance < minDistance) {
					logger.info("Dropped below minDistance of {}, after adding {} words", minDistance, matches.size());
					break;
				}
				if (!universe.contains(word) || searchTerm.equalsIgnoreCase(word)) {
					continue;
				}
				logger.debug(word + " " + wordDistance);
				matches.put(word, wordDistance);
			}
			return matches;
		}
	}
	
	private int[] getSortedDistances(String searchTerm, List<Double> negativeDist) {
		RealVector vec_result;
		if(vocab.containsKey(searchTerm)) {
			logger.info("Word: " + searchTerm + ", Position in vocabulary: " + vocab.get(searchTerm));
			vec_result = W.getRowVector(vocab.get(searchTerm));
		} else {
			throw new IllegalArgumentException("Word outside of dictionary, should have been intercepted prior to this method");
		}

		double d = vec_result.getNorm();
		vec_result = vec_result.mapDivideToSelf(d);

		List<Double> dist = new ArrayList<>();
		
		for (int i = 0; i < W.getRowDimension(); i++) {
			dist.add(i, W.getRowVector(i).dotProduct(vec_result) * -1);
			negativeDist.add(-1 * dist.get(i));
		}

		return IntStream.range(0, dist.size())
                .boxed()
				.sorted((i, j) -> dist.get(i).compareTo(dist.get(j)) )
                .mapToInt(ele -> ele)
				.toArray(); // http://stackoverflow.com/questions/4859261/get-the-indices-of-an-array-after-sorting
	}

	private RealMatrix generate(String vocabFilePath, String vectorFilePath, String universeFilePath) {
		RealMatrix W = null;
		
		try {
	        Scanner vocabInput = new Scanner(new File(vocabFilePath));
	        ArrayList<String> words = new ArrayList<String>();
	        while (vocabInput.hasNextLine()) {
	            String line = vocabInput.nextLine();
	            line = line.split(" ")[0];
	            words.add(line);
	        }
	        vocabInput.close();
	        Scanner vectorInput = new Scanner(new File(vectorFilePath));
	        Map<String, ArrayList<Double>> vectors = new HashMap<>();
	        while (vectorInput.hasNextLine()) {
	            String line = vectorInput.nextLine();
	            String vecArray[] = line.split(" ");
	            String word = vecArray[0];
	            ArrayList<Double> wordVec = new ArrayList<Double>();
	            for (int i = 1; i < vecArray.length; i++) {
                    wordVec.add(Double.parseDouble(vecArray[i]));
	            }
	            vectors.put(word, wordVec);
	        }
	        vectorInput.close();
	        Scanner universeInput = new Scanner(new File(universeFilePath));
	        while (universeInput.hasNextLine()) {
	            String line = universeInput.nextLine();
	            line = line.split(" ")[0];
	            universe.add(line);
	        }
	        universeInput.close();
	        int vocab_size = words.size();
	        for (int i = 0; i < words.size(); i++) {
	        	vocab.put(words.get(i), i);
	        	iVocab.put(i, words.get(i));
	        }

	        int vector_dim = vectors.get(iVocab.get(0)).size();
	        W = MatrixUtils.createRealMatrix(vocab_size, vector_dim);
	        for(String word : vectors.keySet()) {
	        	if (word.equals("<unk>")) {
	        		continue;
	        	}
	        	ArrayList<Double> wordVector = vectors.get(word);
	        	for (int i = 0; i < wordVector.size(); i++) {
	        		W.setEntry(vocab.get(word), i, wordVector.get(i));
	        	}
	        }
	        
	        RealVector d = new ArrayRealVector();
	        for (int i = 0; i < W.getRowDimension(); i++) {
	        	double sum = 0;
	        	for (int j = 0; j < W.getColumnDimension(); j++) {
	        		sum += Math.pow(W.getEntry(i, j), 2);
	        	}
	        	d = d.append(Math.sqrt(sum));
	        }
	        for (int i = 0; i < W.getColumnDimension(); i++) {
	        	W.setColumnVector(i, W.getColumnVector(i).ebeDivide(d));
	        }
	    } catch (FileNotFoundException ex) {
	    	logger.info("Could not find file");
	        ex.printStackTrace();
	    }
		return W;
	}

	@Override
	public void calculateDistances(String searchTerm) {
		calculateDistances(searchTerm, 5);
	}


}
