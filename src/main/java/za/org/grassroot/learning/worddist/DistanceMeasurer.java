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

    public void main() { // Example test
		HashMap<String, Integer> vocab = new HashMap<String, Integer>();
	    HashMap<Integer, String> ivocab = new HashMap<Integer, String>();
	    long startTime=System.currentTimeMillis();
		RealMatrix W = generate(vocab, ivocab);
	    long endTime=System.currentTimeMillis();
	    System.out.println("Build time: " + (endTime - startTime) / 1000);
	    Set<String> a = new HashSet<String>();
	    distance(W, vocab, ivocab, "hello");
    }
    
	private static void distance(RealMatrix W, HashMap<String, Integer> vocab, HashMap<Integer, String> ivocab, 
			String input_term) {
		
		RealVector vec_result = null;
		if(vocab.containsKey(input_term)) {
			System.out.println("Word: " + input_term + ", Position in vocabulary: " + vocab.get(input_term));
			vec_result = W.getRowVector(vocab.get(input_term));
		} else {
			System.out.println("Word outside of dictionary!");
		}
		RealVector vec_norm = vec_result.copy();
		double d = vec_result.getNorm();
		vec_result = vec_result.mapDivideToSelf(d);
		ArrayList<Double> dist = new ArrayList<Double>();
		ArrayList<Double> negativeDist = new ArrayList<Double>();
		for(int i = 0; i < W.getRowDimension(); i++) {
			dist.add(i, W.getRowVector(i).dotProduct(vec_result) * -1);
			negativeDist.add(-1 * dist.get(i));
		}
		int[] a = IntStream.range(0, dist.size())
                .boxed().sorted((i, j) -> dist.get(i).compareTo(dist.get(j)) )
                .mapToInt(ele -> ele).toArray(); // http://stackoverflow.com/questions/4859261/get-the-indices-of-an-array-after-sorting
		for(int i = 0; i < N; i++) {
			int x = a[i];
			System.out.println(ivocab.get(x) + " " + negativeDist.get(x));
		}
	}

	private static RealMatrix generate(HashMap<String, Integer> vocab, HashMap<Integer, String> ivocab) {
		RealMatrix W = null;
		try {
	        Scanner vocabInput = new Scanner(new File("vocab.txt"));
	        ArrayList<String> words = new ArrayList<String>();
	        while (vocabInput.hasNextLine()) {
	            String line = vocabInput.nextLine();
	            line = line.split(" ")[0];
	            words.add(line);
	        }
	        vocabInput.close();
	        Scanner vectorInput = new Scanner(new File("vectors.txt"));
	        HashMap<String, ArrayList<Double>> vectors = new HashMap<String, ArrayList<Double>>();
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
	        int vocab_size = words.size();
	        for (int i = 0; i < words.size(); i++) {
	        	vocab.put(words.get(i), i);
	        	ivocab.put(i, words.get(i));
	        }
	        int vector_dim = vectors.get(ivocab.get(0)).size();
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
	        ex.printStackTrace();
	    }
		return W;
	}

}
