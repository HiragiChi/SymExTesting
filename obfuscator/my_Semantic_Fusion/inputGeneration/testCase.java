public class testCase {
public double run(double x) {

		if (Math.cosh(x)>1) {
			System.out.println("Correct Find Path");
			return 1;
		}
		else{
			System.out.println("The Other Path");
			return 0;
		}
	}

	public static void main(String[] args) {
		testCase num = new testCase();
		num.run(12);
	}
	
}