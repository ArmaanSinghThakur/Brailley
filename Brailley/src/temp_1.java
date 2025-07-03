import java.util.*;

public class temp_1 {
    public static void greet(String wel) {
        System.out.println("Welcome, " + wel);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int steps = sc.nextInt();
        sc.nextLine(); // consume the leftover newline

        String section = sc.nextLine();
        greet("Walmart visitor");
        System.out.println("Walk " + steps + " steps to reach the " + section + " section.");

        String current = speech.readCurrentLocationFromFile();

        System.out.print("Enter destination section: ");
        String desti = sc.nextLine();

        speech.speak("Navigating from " + current + " to " + desti);
    }
}


/* Entracne -- Main bottom Entry (entry/exit near mufti)
*  Grocery  -- World of Titan(G-5/6)
*  Dairy    -- Sephora(G-41)
* Cosmetics -- Punjab Jewellers(G-7/8/9)
*  Pharmacy -- Tanishq(G-19)
*  Clothing -- Calvin Kilein(G-24/25)*/



