import com.sun.speech.freetts.*;

import java.io.File;
import java.util.Scanner;

public class speech {
    static Voice voice;

    static {
        System.setProperty("freetts.voices",
                "com.sun.speech.freetts.en.us.cmu_us_kal.KevinVoiceDirectory");

        VoiceManager vm = VoiceManager.getInstance();
        voice = vm.getVoice("kevin16");

        if (voice != null) {
            voice.allocate();
        } else {
            System.out.println("Voice not found. Please check the JAR files and classpath.");
        }
    }

    public static void speak(String text) {
        if (voice != null) {
            voice.speak(text);
        } else {
            System.out.println("Voice is not allocated.");
        }
    }

    public static String readCurrentLocationFromFile() {
        try (Scanner s = new Scanner(new File("current_location.txt"))) {
            return s.hasNextLine() ? s.nextLine().trim() : null;
        } catch (Exception e) {
            return null;
        }
    }

    public static double[] readGPSLocationFromFile() {
        try (Scanner sc = new Scanner(new File("current_gps.txt"))) {
            if (sc.hasNextLine()) {
                String[] parts = sc.nextLine().trim().split(",");
                return new double[]{
                        Double.parseDouble(parts[0]), Double.parseDouble(parts[1])
                };
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public static double[] readGPSFromFile() {
        try (Scanner sc = new Scanner(new File("gps_coordinates.txt"))) {
            double lat = sc.nextDouble();
            double lon = sc.nextDouble();
            return new double[]{lat, lon};
        } catch (Exception e) {
            return null;
        }
    }
}
