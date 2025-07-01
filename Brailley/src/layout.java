import java.util.*;

public class layout {
    Map<String, section> area = new HashMap<>();

    public void addsection(String nameofsection) {
        area.putIfAbsent(nameofsection, new section(nameofsection));
    }

    public void adddistance(String from, String destination, int steps) {
        section fromsection = area.get(from);
        section destinationsection = area.get(destination);
        if (fromsection != null && destinationsection != null) {
            fromsection.adddistance(destinationsection, steps);
            destinationsection.adddistance(fromsection, steps);
        }
    }

    public void printMap() {
        for (String name : area.keySet()) {
            System.out.println(name + " connects to: ");
            for (distance edge : area.get(name).listofpaths) {
                System.out.println("  → " + edge.destination.nameofsection + " (" + edge.steps + " steps)");
            }
        }
    }

    public List<String> findshortestpath(String startnameofsection, String endnameofsection) {
        Map<String, Integer> distances = new HashMap<>();
        Map<String, String> previous = new HashMap<>();
        Set<String> visited = new HashSet<>();
        PriorityQueue<sectionpathcovered> queue = new PriorityQueue<>(Comparator.comparingInt(nd -> nd.gap));

        for (String nameofsection : area.keySet()) {
            distances.put(nameofsection, Integer.MAX_VALUE);
        }

        distances.put(startnameofsection, 0);
        queue.add(new sectionpathcovered(startnameofsection, 0));

        while (!queue.isEmpty()) {
            sectionpathcovered current = queue.poll();
            if (visited.contains(current.nameofsection)) continue;
            visited.add(current.nameofsection);

            section currentsection = area.get(current.nameofsection);
            for (distance edge : currentsection.listofpaths) {
                int newDist = distances.get(current.nameofsection) + edge.steps;
                String neighbourName = edge.destination.nameofsection;
                if (newDist < distances.get(neighbourName)) {
                    distances.put(neighbourName, newDist);
                    previous.put(neighbourName, current.nameofsection);
                    queue.add(new sectionpathcovered(neighbourName, newDist));
                }
            }
        }

        LinkedList<String> path = new LinkedList<>();
        String current = endnameofsection;
        while (current != null) {
            path.addFirst(current);
            current = previous.get(current);
        }

        if (!path.isEmpty() && path.getFirst().equals(startnameofsection)) {
            return path;
        } else {
            return Collections.emptyList();
        }
    }

    public List<distance> getlistofpaths(String currentLocation) {
        section currentSection = area.get(currentLocation);
        if (currentSection != null) {
            return currentSection.listofpaths;
        }
        return Collections.emptyList();
    }

    public String voice(List<String> path) {
        if (path.isEmpty()) return "No path found.";

        StringBuilder instructions = new StringBuilder();
        instructions.append("Start from ").append(path.get(0)).append(". ");

        for (int i = 1; i < path.size(); i++) {
            String from = path.get(i - 1);
            String destination = path.get(i);
            section fromsection = area.get(from);

            int step = -1;
            for (distance edge : fromsection.listofpaths) {
                if (edge.destination.nameofsection.equals(destination)) {
                    step = edge.steps;
                    break;
                }
            }

            if (i == path.size() - 1) {
                instructions.append("Then reach ").append(destination)
                        .append(" (").append(step).append(" steps).");
            } else {
                instructions.append("Move to ").append(destination)
                        .append(" (").append(step).append(" steps). ");
            }
        }

        return instructions.toString();
    }
}

class sectionpathcovered {
    String nameofsection;
    int gap;

    sectionpathcovered(String nameofsection, int gap) {
        this.nameofsection = nameofsection;
        this.gap = gap;
    }
}

class LiveTracker {
    private String currentLocation;
    private layout graph;

    public LiveTracker(layout graph, String startLocation) {
        this.graph = graph;
        this.currentLocation = startLocation;
    }

    public String getCurrentlocation() {
        return currentLocation;
    }

    public boolean reach(String nextsection) {
        List<distance> edges = graph.getlistofpaths(currentLocation);
        for (distance edge : edges) {
            if (edge.destination.nameofsection.equals(nextsection)) {
                currentLocation = nextsection;
                return true;
            }
        }
        return false;
    }

    public void reset(String location) {
        currentLocation = location;
    }
}
