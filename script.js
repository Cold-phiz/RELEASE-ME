function addTerminalLine(message) {
    const line = document.createElement("div");
    line.className = "terminal-line";
    line.textContent = message;

    const terminalOutput = document.getElementById("terminal-output");
    terminalOutput.prepend(line);

    setTimeout(() => {
        line.remove();
    }, 5000); // Remove line after 5 seconds
}

// Example usage
addTerminalLine("Starting server...");
addTerminalLine("Connected to database.");
addTerminalLine("Listening on port 3000.");
