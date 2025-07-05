import java.util.*;
import java.util.ArrayList;
import java.util.List;

public class section {
    Scanner sc = new Scanner(System.in);

    String nameofsection;
    List<distance> listofpaths = new ArrayList<>();
    double latitude, longitude;

    public section(String nameofsection, double lat, double lon) {
        this.nameofsection = nameofsection;
        this.latitude = lat;
        this.longitude = lon;
    }

    public void adddistance(section destination, int steps) {
        listofpaths.add(new distance(destination, steps));
    }
}