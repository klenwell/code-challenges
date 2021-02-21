/**
 * Simple exercise that prompts user to input number from command line.
 *
 * Test Online:
 * https://repl.it/languages/java10
 *
 * $ javac Main.java
 * $ java Main
 */
import java.util.Scanner;

class Main {
    private Scanner scanner;

    public static void main(String args[]) {
        Main main = new Main();
        main.loop();
    }

    public Main() {
        this.scanner = new Scanner(System.in);
    }

    public void loop() {
        this.output("\nPlease enter a number or q to quit: ");
        String input = this.readInput();

        try {
            this.quitIfRequested(input);
            this.validate(input);
            this.outputValid(input);
        }
        catch (Exception e) {
            this.outputError(input, e);
        }

        this.loop();
    }

    private String readInput() {
        return this.scanner.nextLine();
    }

    private void validate(String input) {
        // Will raise exception if string is not numeric.
        Double.parseDouble(input);
    }

    private void outputValid(String input) {
        String f = "Valid input: %s";
        this.output(String.format(f, input));
    }

    private void outputError(String input, Exception e) {
        String f = "Invalid input: %s (%s)";
        this.output(String.format(f, input, e));
    }

    private void output(String message) {
        System.out.println(message);
    }

    private void quitIfRequested(String input) {
        boolean quitRequested = input.toLowerCase().charAt(0) == 'q';
        if ( quitRequested ) {
            this.quit();
        }
    }

    private void quit() {
      this.scanner.close();
      System.exit(0);
    }
}
