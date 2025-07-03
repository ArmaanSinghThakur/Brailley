import java.util.*;

public class distance {

    section destination;
    int steps;

    public distance(section destination, int steps) {
        this.destination = destination;
        this.steps = steps;
    }

    @Override
    public String toString() {
        return "→ " + destination.nameofsection + " (" + steps + " steps)";
    }
}
