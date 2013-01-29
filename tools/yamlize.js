var lastInput = "";

function cleaned(str) {
    str = str.replace(/\s/g," ");
    str = str.replace(/\u2018/g,"'"); // &lsquo;
    return str;
}

function proc() {
    var input = document.getElementById("input");
    var output = document.getElementById("output");
    var blockMode = false;

    if(input.value === lastInput) {
        return;
    }
    lastInput = input.value;

    lines = input.value.split("\n");

    output.value = ""
        for(var i = 0, even = true, firstLine = ""; i < lines.length; i++) {
            if(lines[i] === "====") {
                blockMode = !blockMode;
                if(blockMode) {
                    output.value += "    - |\n";
                }
                even = true;
            } else {
                if(blockMode) {
                    output.value += "       " + cleaned(lines[i]) + "\n";
                } else {
                    var l = lines[i].split("<==>");

                    if(l.length === 2 && even) {
                        lines.splice(i, 1, l[0], l[1]);
                    }

                    var line = JSON.stringify(cleaned(lines[i].trim())).slice(1, -1);

                    if(line.search(/[-?:,[\]{}#&*!|>'"%@`]/) !== -1) {
                        line = '"' + line + '"';
                }
                if(even) {
                    if(line === "") {
                        even = !even;
                    } else {
                        firstLine = line;
                    }
                } else {
                    output.value += "    - [" + firstLine + ", " + line + "]\n";
                }
                even = !even;
                }
            }
        }
}
setInterval(proc, 500);
