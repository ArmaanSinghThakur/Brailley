import java.util.*;
import java.util.ArrayList;
import java.util.List;

public class section{
    Scanner sc = new Scanner(System.in);

    String nameofsection;
    List<distance> listofpaths = new ArrayList<>();

    public section(String nameofsection){
        this.nameofsection = nameofsection;
    }
public void adddistance(section destination, int steps){
        listofpaths.add(new distance(destination, steps));
}
}
