import java.util.*;

public class temp_1 {
    public static void greet(String wel) {
        System.out.println("welcome, " + wel);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
       greet("walmart visiter");

        layout layoutMap = new layout();
       navigator nav = new navigator(layoutMap);

       double[] gps = speech.readGPSLocationFromFile();
       if (gps == null) {
           System.out.println("unable to find path: ");
           return;
       }

       section current = nav.getNearestSection(gps[0], gps[1]);
        System.out.println("you are closest to: " + current.nameofsection);

        System.out.println("enter your destination: ");
        String destName = sc.nextLine().trim();

        section destination = layoutMap.getSectionByName(destName);
        if (destination == null) {
            System.out.println("unknown desination.");
            return;
        }

        List<section> path = nav.findPath(current, destination);
        if (path.isEmpty()) {
            System.out.println("no path found.");
        }
        else {
            for (section s : path) {
                System.out.println("walk to " + s.nameofsection);
                speech.speak("walk to " + s.nameofsection);
            }
        }
    }
}


/* Entracne -- Main bottom Entry (entry/exit near mufti)
*  Grocery  -- World of Titan(G-5/6)
*  Dairy    -- Sephora(G-41)
* Cosmetics -- Punjab Jewellers(G-7/8/9)
*  Pharmacy -- Tanishq(G-19)
*  Clothing -- Calvin Kilein(G-24/25)*/



