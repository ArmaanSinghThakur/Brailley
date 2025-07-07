import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

public class store_navigation {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        speech Speech = new speech();

        layout store = new layout();

        store.addsection("Entrance", 23.232690574985387,77.43031939481776);
        store.addsection("Grocery",  23.23259914588621, 77.43018134951647); //World of Titan
        store.addsection("Dairy",    23.23272298279288, 77.43013270656009); //Sephora
        store.addsection("Cosmetics",23.232548585222627,77.43009841726297); //Punjab Jewellers
        store.addsection("A",        23.232632039934174,77.43008918320588); // midpoint
        store.addsection("B",        23.232701051820214,77.43005163227951); // midpoint
        store.addsection("C",        23.23272019882376, 77.4299712114929);  // midpoint
        store.addsection("D",        23.232699864971096,77.42990750902858); // midpoint
        store.addsection("E",        23.23251522714504, 77.43004678420789); // midpoint
        store.addsection("F",        23.232494277082807,77.4299696706984);  // midpoint
        store.addsection("Pharmacy", 23.23244677569446, 77.42998519020539); //Tanishq
        store.addsection("Clothing", 23.232754864626784,77.42986784356071); //Calvin Klein

        double[] gps = Speech.readGPSLocationFromFile();
        if (gps == null) {
            System.out.println("no coordinates found");
            return;
        }

        store.adddistance("Entrance", "Grocery", 7);
        store.adddistance("Entrance", "Dairy", 5);
        store.adddistance("Entrance", "Cosmetics", 5);
        store.adddistance("Grocery", "Dairy", 4);
        store.adddistance("Grocery", "Pharmacy", 3);
        store.adddistance("Cosmetics", "Dairy", 4);
        store.adddistance("Cosmetics", "Clothing", 3);
        store.adddistance("Clothing", "Pharmacy", 4);
        store.adddistance("Grocery", "Cosmetics", 2);
        store.adddistance("Dairy", "B", 2);
        store.adddistance("Cosmetics", "A", 1);
        store.adddistance("A", "B", 1);
        store.adddistance("B", "C", 1);
        store.adddistance("C", "D", 1);
        store.adddistance("D", "Clothing", 1);
        store.adddistance("Cosmetics", "Pharmacy", 3);
        store.adddistance("A", "Pharmacy", 1);


        System.out.println("🗺️  Mall Map Layout:");
        store.printMap();

        Map<String, List<Connection>> storeMap = new HashMap<>();
        storeMap.put("Entrance", List.of(
                new Connection("Grocery", "right", 7),
                new Connection("Dairy", "straight", 5),
                new Connection("Cosmetics", "left", 5)
        ));
        storeMap.put("Grocery", List.of(
                new Connection("Pharmacy", "right", 3),
                new Connection("Dairy", "left", 4)
        ));
        storeMap.put("Cosmetics", List.of(
                new Connection("Clothing", "right", 3),
                new Connection("Dairy", "straight", 4)
        ));
        storeMap.put("Clothing", List.of(
                new Connection("Pharmacy", "left", 4)
        ));

        // nearest section
        String currentSection = store.mapCoordinatesToSection(gps[0], gps[1]);
        System.out.println("starting near: " + currentSection);
        speech.speak("starting near: " + currentSection);

        //asking user their destination
        System.out.println("please tell me your destination: ");
        String destination = sc.nextLine().trim();

        var path = store.findshortestpath(currentSection, destination);
        if (!path.isEmpty()) {
            System.out.println("Path: " + String.join(" -> ", path));
            for (String next : path) {
              String instr = "walk to: " + next;
                System.out.println(instr);
                speech.speak(instr);
                writeCurrentLocationToFile(next);
                waitForGPSChange(next);
            }
        } else {
            System.out.println("no valid path is found.");
        }

        LiveTracker tracker = new LiveTracker(store, "Entrance");
        System.out.println("Smart stick is on work.");
        System.out.println("Current Location: " + tracker.getCurrentlocation());

        while (true) {
            System.out.println("\nEnter the section to move or type 'exit': ");
            String input = sc.nextLine();

            if (input.equalsIgnoreCase("exit")) break;

            boolean directMove = store.getlistofpaths(tracker.getCurrentlocation())
                    .stream().anyMatch(e -> e.destination.nameofsection.equals(input));

            if (directMove) {
                tracker.reach(input);
                System.out.println("Moved to: " + tracker.getCurrentlocation());
            } else {
                var altPath = store.findshortestpath(tracker.getCurrentlocation(), input);
                if (!altPath.isEmpty()) {
                    String voice = store.voice(altPath);
                    System.out.println("Navigate:\n" + voice);
                    Speech.speak(voice);
                } else {
                    System.out.println("No path found.");
                }
            }
        }

        // Start tracking using GPS
        System.out.println("\nSwitching to GPS tracking...\n");
        String previousLocation = "";

        while (true) {
            gps = readGPSFromFile();
            if (gps == null) {
                System.out.println("Failed to read GPS coordinates.");
                continue;
            }

            String current = store.mapCoordinatesToSection(gps[0], gps[1]);
            if (current == null) {
                System.out.println("No section mapped to GPS location.");
                continue;
            }

            if (!current.equals(previousLocation)) {
                previousLocation = current;

                List<String> newPath = store.findshortestpath(current, destination);
                if (!newPath.isEmpty()) {
                    String voice = store.voice(newPath);
                    System.out.println("You are now at: " + current);
                    System.out.println("Voice Directions: " + voice);
                    Speech.speak("Now at " + current + ". " + voice);
                } else {
                    Speech.speak("Cannot find a path from " + current + " to " + destination);
                }
            }

            try {
                Thread.sleep(3000);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }
    }

    public static void waitForGPSChange(String targetSection) {
        try {
            Thread.sleep(3000);
        }
        catch (InterruptedException e) {
        }
    }

    public static void writeCurrentLocationToFile(String location) {
        try (FileWriter writer = new FileWriter("current_location.txt")){
            writer.write(location);
        }
        catch (IOException e) {
            System.out.println("failed to write location");
        }
    }

    public static Connection getConnection(String from, String to, Map<String, List<Connection>> storeMap) {
        List<Connection> connections = storeMap.get(from);
        if (connections != null) {
            for (Connection c : connections) {
                if (c.location.equals(to)) return c;
            }
        }
        return null;
    }

    public static void simulateWalking(List<String> path, Map<String, List<Connection>> storeMap,
                                       speech Speech, Scanner sc) {
        for (int i = 0; i < path.size() - 1; i++) {
            String from = path.get(i);
            String to = path.get(i + 1);
            Connection conn = getConnection(from, to, storeMap);

            if (conn == null) {
                System.out.println("No connection found between " + from + " and " + to);
                continue;
            }

            String instruction = "Turn " + conn.direction + " and walk " + conn.steps + " steps to " + to;
            System.out.println(instruction);
            Speech.speak(instruction);

            for (int s = 1; s <= conn.steps; s++) {
                System.out.print("Type 'step' to move forward: ");
                sc.nextLine();
                System.out.println("Step " + s + "/" + conn.steps);
            }

            writeCurrentLocationToFile(to);
        }
    }

    public static double[] readGPSFromFile() {
        try (Scanner s = new Scanner(new File("gps_coordinates.txt"))) {
            double lat = s.nextDouble();
            double lon = s.nextDouble();
            return new double[] { lat, lon };
        } catch (Exception e) {
            return null;
        }
    }
}
