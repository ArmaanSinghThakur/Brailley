import com.sun.speech.freetts.*;

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
        try (java.util.Scanner s = new java.util.Scanner(new java.io.File("current_location.txt"))) {
            return s.hasNextLine() ? s.nextLine().trim() : null;
        } catch (Exception e) {
            return null;
        }
    }
}
