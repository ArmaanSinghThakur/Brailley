import java.util.*;

public class temp_1 {
    public static void greet(String wel) {
        System.out.println("Welcome, " + wel);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int steps = sc.nextInt();
        String section = sc.next();
        greet("Walmart visitor");
        System.out.println("Walk " + steps + " steps to reach the " + section + " section.");

        String current = speech.readCurrentLocationFromFile();
        System.out.print("Enter destination section: ");
        String desti = sc.nextLine();
        speech.speak("Navigating from " + current + " to " + desti);

    }
}

