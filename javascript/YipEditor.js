/**
 * Use: let myEditor = new YipEditor(); to create a new HTML editor.
 * @author Alexa N <alexa.nc.kitsune@gmail.com>
 * @param {string} identifier - Set the id (the one you want) of your new editor.
 * @param {Boolean} editable - Set the editor textarea as editable (true), or non editable / only read (false).
 * @param {getElementById} putIn - The id of the element where you will append the editor.
 *
 * myEditor.runEditor(); sets the editor in HTML.
 *
 * myEditor.getCode(); extracts the code, returns a string.
 */

class YipEditor{

	constructor(identifier, editable, putIn=""){
		this._identifier = identifier;
		this._editable = editable;
        this._putIn = putIn;
	}

	runEditor(){
        //Creating elements:
        let yipMasterContainer = document.createElement("div");
		let yipCode = document.createElement("textarea");
        let yipRun = document.createElement("button");
        yipRun.innerHTML = '▶';
        let yipConsole = document.createElement("div");
        let yipInvisible = document.createElement("div");

        //Setting "id"s:
        yipMasterContainer.setAttribute("id", this._identifier);
        yipCode.setAttribute("id", `${this._identifier}_Code`);
        yipRun.setAttribute("id", `${this._identifier}_Run`);
        yipConsole.setAttribute("id", `${this._identifier}_Console`);
        yipInvisible.setAttribute("id", `${this._identifier}_Invisible`);
        
        //Setting classes(for CSS): 
        yipMasterContainer.setAttribute("class", 'yipMaster');
        yipRun.setAttribute("class", 'yipRun');
        yipConsole.setAttribute("class", 'yipConsole');
        yipInvisible.setAttribute("class", 'yipInvisible');

        //Putting elements:
        document.getElementById(this._putIn).appendChild(yipMasterContainer); //<- This is a test
        document.getElementById(this._identifier).appendChild(yipCode);
        document.getElementById(this._identifier).appendChild(yipRun);
        document.getElementById(this._identifier).appendChild(yipConsole);
        document.getElementById(this._identifier).appendChild(yipInvisible);
        
        //Setting codemirror:
        var editor = CodeMirror.fromTextArea(
            document.getElementById(`${this._identifier}_Code`),
            {
                mode:"javascript",
                theme:"dracula",
                matchBrackets:true,
                autoCloseBrackets: true,
                lineNumbers: true
            }
        );
		
        //Working YipEditor:
        yipRun.onclick = function(){
            function display(x){return x};
            setTimeout(function () {
                let inCode = editor.getValue();
                inCode = inCode.replaceAll("eval","display");  //<- Eliminando valores nativos JS...
                inCode = inCode.replaceAll("instanceof","");
                inCode = inCode.replaceAll("document.","");
                inCode = inCode.replaceAll("getElementById","");
                inCode = inCode.replaceAll("getElementsBy","");
                inCode = inCode.replaceAll("set","");
                inCode = inCode.replaceAll("onclick","");
                inCode = inCode.replaceAll("onclic","");
                inCode = inCode.replaceAll("HTML","");
                inCode = inCode.replaceAll("import","");
                inCode = inCode.replaceAll("./","");
                inCode = inCode.replaceAll("execute",""); //<- Eliminando valores del proyecto...
                inCode = inCode.replaceAll("setTime","");
                inCode = inCode.replaceAll("identifier","");
                inCode = inCode.replaceAll("editable","");
                inCode = inCode.replaceAll("putIn","");
                inCode = inCode.replaceAll("console.log","display"); //<- Agregando (+mod) características propias...
                inCode = inCode.replaceAll("document.write","display");
                inCode = inCode.replaceAll("print","display");

                console.log(eval(inCode));//
                yipInvisible.innerHTML = inCode;
                return yipConsole.innerHTML = "🦊>> "+eval(inCode);
            });     
        };

	}

    getCode(){
        return document.getElementById(`${this._identifier}_Invisible`).innerHTML;
    }

}