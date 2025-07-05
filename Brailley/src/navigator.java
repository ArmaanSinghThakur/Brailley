import java.util.*;

public class navigator {
    layout layoutMap;

    public navigator(layout layoutMap) {
        this.layoutMap = layoutMap;
    }

    public section getNearestSection(double userLat, double userLon) {
        section nearest = null;
        double minDist = Double.MAX_VALUE;

        for (section s : layoutMap.map.values()) {
            double d = distance(userLat, userLon, s.latitude, s.longitude);
            if (d < minDist) {
                minDist = d;
                nearest = s;
            }
        }
        return nearest;
    }

    public List<section> findPath(section start, section end) {
        Map<section, section> prev = new HashMap<>();
        Queue<section> queue = new LinkedList<>();
        Set<section> visited = new HashSet<>();

        queue.add(start);
        visited.add(start);

        while (!queue.isEmpty()) {
            section current = queue.poll();

            if (current == end)
                break;

            for (distance d : current.listofpaths) {
             section neighbor = d.destination;
             if (!visited.contains(neighbor)) {
                 visited.add(neighbor);
                 prev.put(neighbor, current);
                 queue.add(neighbor);
             }
            }
        }

        List<section> path = new LinkedList<>();
        section step = end;

        while (step != null) {
         path.add(0, step);
         step = prev.get(step);
        }
        return path.get(0) == start ? path : new ArrayList<>();
    }
    private double distance(double lat1, double lon1, double lat2, double lon2) {
        return Math.sqrt(Math.pow(lat1 - lat2, 2) + Math.pow(lon1 - lon2, 2));
    }
}
