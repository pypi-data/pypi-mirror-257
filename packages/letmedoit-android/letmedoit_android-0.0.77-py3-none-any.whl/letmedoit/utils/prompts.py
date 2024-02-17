from letmedoit import config
import pydoc, textwrap, re, tiktoken
import speech_recognition as sr
from prompt_toolkit import prompt
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit.styles import Style
from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings, ConditionalKeyBindings
from letmedoit.utils.prompt_shared_key_bindings import prompt_shared_key_bindings
from letmedoit.utils.prompt_multiline_shared_key_bindings import prompt_multiline_shared_key_bindings
from letmedoit.utils.promptValidator import NumberValidator
from letmedoit.utils.shared_utils import SharedUtil
from prompt_toolkit.clipboard.pyperclip import PyperclipClipboard

class Prompts:

    def __init__(self):
        config.multilineInput = False
        config.clipboard = PyperclipClipboard()
        config.promptStyle1 = self.promptStyle1 = Style.from_dict({
            # User input (default text).
            "": config.terminalCommandEntryColor1,
            # Prompt.
            "indicator": config.terminalPromptIndicatorColor1,
        })
        config.promptStyle2 = self.promptStyle2 = Style.from_dict({
            # User input (default text).
            "": config.terminalCommandEntryColor2,
            # Prompt.
            "indicator": config.terminalPromptIndicatorColor2,
        })
        self.inputIndicator = [
            ("class:indicator", ">>> "),
        ]
        self.shareKeyBindings()
        config.showKeyBindings = self.showKeyBindings
        config.terminalColors = {
            "ansidefault": "ansidefault",
            "ansiblack": "ansiwhite",
            "ansired": "ansibrightred",
            "ansigreen": "ansibrightgreen",
            "ansiyellow": "ansibrightyellow",
            "ansiblue": "ansibrightblue",
            "ansimagenta": "ansibrightmagenta",
            "ansicyan": "ansibrightcyan",
            "ansigray": "ansibrightblack",
            "ansiwhite": "ansiblack",
            "ansibrightred": "ansired",
            "ansibrightgreen": "ansigreen",
            "ansibrightyellow": "ansiyellow",
            "ansibrightblue": "ansiblue",
            "ansibrightmagenta": "ansimagenta",
            "ansibrightcyan": "ansicyan",
            "ansibrightblack": "ansigray",
        }

    def getToolBar(self, multiline=False):
        if multiline:
            return f" [ctrl+q] exit [escape+enter] send "
        return f" [ctrl+q] exit [enter] send "

    def shareKeyBindings(self):
        this_key_bindings = KeyBindings()

        @this_key_bindings.add("c-f")
        def _(event):
            # reference: https://github.com/Uberi/speech_recognition/blob/master/examples/microphone_recognition.py
            def voiceTyping():
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    run_in_terminal(lambda: config.print2("Listensing to your voice ..."))
                    if config.voiceTypingAdjustAmbientNoise:
                        r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                run_in_terminal(lambda: config.print2("Processing to your voice ..."))
                if config.voiceTypingModel == "google":
                    # recognize speech using Google Speech Recognition
                    try:
                        # check google.recognize_legacy in SpeechRecognition package
                        # check availabl languages at: https://cloud.google.com/speech-to-text/docs/speech-to-text-supported-languages
                        # config.voiceTypingLanguage should be code list in column BCP-47 at https://cloud.google.com/speech-to-text/docs/speech-to-text-supported-languages
                        return r.recognize_google(audio, language=config.voiceTypingLanguage)
                    except sr.UnknownValueError:
                        #return "[Speech unrecognized!]"
                        return ""
                    except sr.RequestError as e:
                        return "[Error: {0}]".format(e)
                if config.voiceTypingModel == "whisper":
                    # recognize speech using whisper
                    try:
                        # check availabl languages at: https://github.com/openai/whisper/blob/main/whisper/tokenizer.py
                        # config.voiceTypingLanguage should be uncapitalized full language name like "english" or "chinese"
                        return r.recognize_whisper(audio, model="base" if config.voiceTypingLanguage == "english" else "large", language=config.voiceTypingLanguage)
                    except sr.UnknownValueError:
                        return ""
                    except sr.RequestError as e:
                        return "[Error]"

            if config.pyaudioInstalled:
                buffer = event.app.current_buffer
                buffer.text = f"{buffer.text}{' ' if buffer.text else ''}{voiceTyping()}"
                buffer.cursor_position = buffer.cursor_position + buffer.document.get_end_of_line_position()
            else:
                run_in_terminal(lambda: config.print2("Install PyAudio first to enable voice entry!"))
        @this_key_bindings.add("escape", "f")
        def _(event):
            buffer = event.app.current_buffer
            buffer.text = ".voicetypingconfig"
            buffer.validate_and_handle()
        @this_key_bindings.add("c-q")
        def _(event):
            buffer = event.app.current_buffer
            buffer.text = config.exit_entry
            buffer.validate_and_handle()
        @this_key_bindings.add("c-i") # add path
        def _(event):
            buffer = event.app.current_buffer
            config.addPathAt = buffer.cursor_position
            buffer.validate_and_handle()
        @this_key_bindings.add("c-n")
        def _(event):
            buffer = event.app.current_buffer
            config.defaultEntry = buffer.text
            buffer.text = ".new"
            buffer.validate_and_handle()
        @this_key_bindings.add("c-y")
        def _(event):
            buffer = event.app.current_buffer
            config.predefinedContextTemp = config.predefinedContext
            config.predefinedContext = "[none]"
            buffer.text = ".new"
            buffer.validate_and_handle()
            run_in_terminal(lambda: config.print3("Predefined context temporarily changed to: [none]"))
        @this_key_bindings.add("c-s")
        def _(event):
            buffer = event.app.current_buffer
            buffer.text = ".export"
            buffer.validate_and_handle()
        @this_key_bindings.add("escape", "i")
        def _(_):
            run_in_terminal(lambda: print(SharedUtil.getDeviceInfo(True)))
        @this_key_bindings.add("escape", "c")
        def _(event):
            try:
                try:
                    encoding = tiktoken.encoding_for_model(config.chatGPTApiModel)
                except:
                    encoding = tiktoken.get_encoding("cl100k_base")
                currentInput = event.app.current_buffer.text
                no_function_call_pattern = "\[NO_FUNCTION_CALL\]|\[CHAT\]|\[CHAT_[^\[\]]+?\]"
                #if "[NO_FUNCTION_CALL]" in currentInput:
                if re.search(no_function_call_pattern, currentInput):
                    availableFunctionTokens = 0
                    #currentInput = currentInput.replace("[NO_FUNCTION_CALL]", "")
                    currentInput = re.sub(no_function_call_pattern, "", currentInput)
                else:
                    availableFunctionTokens = SharedUtil.count_tokens_from_functions(config.chatGPTApiFunctionSignatures)
                currentInputTokens = len(encoding.encode(config.fineTuneUserInput(currentInput)))
                loadedMessageTokens = SharedUtil.count_tokens_from_messages(config.currentMessages)
                selectedModelLimit = SharedUtil.tokenLimits[config.chatGPTApiModel]
                estimatedAvailableTokens = selectedModelLimit - availableFunctionTokens - loadedMessageTokens - currentInputTokens

                content = f"""{config.divider}
# Current model
{config.chatGPTApiModel}
# Token Count
Model limit: {selectedModelLimit}
Active functions: {availableFunctionTokens}
Loaded messages: {loadedMessageTokens}
Current input: {currentInputTokens}
{config.divider}
Available tokens: {estimatedAvailableTokens}
{config.divider}
"""
            except:
                content = "Required package 'tiktoken' not found!"
            run_in_terminal(lambda: config.print(content))
        @this_key_bindings.add("c-g")
        def _(_):
            config.launchPager()
        @this_key_bindings.add("escape", "d")
        def _(_):
            config.developer = not config.developer
            config.saveConfig()
            run_in_terminal(lambda: config.print3(f"Developer mode: {'enabled' if config.developer else 'disabled'}!"))
        @this_key_bindings.add("c-l")
        def _(_):
            config.toggleMultiline()
        @this_key_bindings.add("c-o")
        def _(event):
            buffer = event.app.current_buffer
            config.defaultEntry = buffer.text
            buffer.text = ".context"
            buffer.validate_and_handle()
        @this_key_bindings.add("escape", "!")
        @this_key_bindings.add("escape", "t")
        def _(event):
            buffer = event.app.current_buffer
            buffer.text = ".system"
            buffer.validate_and_handle()
        @this_key_bindings.add("c-k")
        def _(_):
            run_in_terminal(self.showKeyBindings)
        @this_key_bindings.add("c-b")
        def _(_):
            if config.tts:
                config.ttsInput = not config.ttsInput
                config.saveConfig()
                run_in_terminal(lambda: config.print3(f"Input Audio: '{'enabled' if config.ttsInput else 'disabled'}'!"))
        @this_key_bindings.add("c-p")
        def _(_):
            if config.tts:
                config.ttsOutput = not config.ttsOutput
                config.saveConfig()
                run_in_terminal(lambda: config.print3(f"Response Audio: '{'enabled' if config.ttsOutput else 'disabled'}'!"))
        @this_key_bindings.add("escape", "r")
        def _(_):
            print(f"Restarting {config.letMeDoItName} ...")
            config.restartApp()
        @this_key_bindings.add("escape", "w")
        def _(_):
            config.displayImprovedWriting = not config.displayImprovedWriting
            config.saveConfig()
            run_in_terminal(lambda: config.print3(f"Improved Writing Display: '{'enabled' if config.displayImprovedWriting else 'disabled'}'!"))
        @this_key_bindings.add("c-w")
        def _(_):
            config.wrapWords = not config.wrapWords
            config.saveConfig()
            run_in_terminal(lambda: config.print3(f"Word Wrap: '{'enabled' if config.wrapWords else 'disabled'}'!"))
        @this_key_bindings.add("escape", "m")
        def _(_):
            config.mouseSupport = not config.mouseSupport
            config.saveConfig()
            run_in_terminal(lambda: config.print3(f"Entry Mouse Support: '{'enabled' if config.mouseSupport else 'disabled'}'!"))
        # edit the last response in built-in or custom text editor
        @this_key_bindings.add("escape", "p")
        def _(event):
            buffer = event.app.current_buffer
            buffer.text = ".editresponse"
            buffer.validate_and_handle()

        conditional_prompt_multiline_shared_key_bindings = ConditionalKeyBindings(
            key_bindings=prompt_multiline_shared_key_bindings,
            filter=Condition(lambda: config.multilineInput),
        )
        self.prompt_shared_key_bindings = merge_key_bindings([
            this_key_bindings,
            conditional_prompt_multiline_shared_key_bindings,
            prompt_shared_key_bindings,
        ])
    def showKeyBindings(self):
        bindings = {
            "enter": "complete entry",
            "esc+enter": "new line",
            "ctrl+q": "quit / exit current feature",
            "ctrl+z": "cancel",
            "ctrl+a": "select / unselect all",
            "ctrl+c": "copy [w/ mouse support]",
            "ctrl+v": "paste [w/ mouse support]",
            "ctrl+x": "cut [w/ mouse support]",
            "ctrl+n": "new chat",
            "ctrl+y": "new chat without context",
            "ctrl+s": "export chat",
            "ctrl+o": "change predefined context",
            "ctrl+g": "pager view",
            "ctrl+d": "forward delete",
            "ctrl+h": "backspace",
            "ctrl+k": "show key bindings",
            "ctrl+f": "activate voice typing",
            "esc+f": "change voice typing configs",
            "ctrl+b": "toggle input audio",
            "ctrl+p": "toggle response audio",
            "ctrl+l": "toggle multi-line entry",
            "ctrl+w": "toggle word wrap",
            "ctrl+i or tab": "insert a file or folder path",
            "shift+tab": f"insert '{config.terminalEditorTabText}' [configurable]",
            "esc+i": "display device information",
            "esc+c": "count current message tokens",
            "esc+w": "toggle improved writing feature",
            "esc+m": "toggle mouse support",
            "esc+t": "system command prompt",
            "esc+b": "move cursor to line beginning",
            "esc+e": "move cursor to line end",
            "esc+a": "move cursor to entry beginning",
            "esc+z": "move cursor to entry end",
            "esc+s": "swap text brightness",
            "esc+d": "swap developer mode",
            "ctrl+r": "reverse-i-search",
            "esc+r": "restart letmedoit",
        }
        textEditor = config.customTextEditor.split(" ", 1)[0]
        bindings["ctrl+e"] = f"""edit current input with '{config.customTextEditor if textEditor and SharedUtil.isPackageInstalled(textEditor) else "eTextEdit"}'"""
        bindings["esc+p"] = f"""edit the previous response with '{config.customTextEditor if textEditor and SharedUtil.isPackageInstalled(textEditor) else "eTextEdit"}'"""
        multilineBindings = {
            "enter": "new line",
            "esc+enter": "complete entry",
            "esc+1": "go up 10 lines",
            "esc+2": "go up 20 lines",
            "esc+3": "go up 30 lines",
            "esc+4": "go up 40 lines",
            "esc+5": "go up 50 lines",
            "esc+6": "go up 60 lines",
            "esc+7": "go up 70 lines",
            "esc+8": "go up 80 lines",
            "esc+9": "go up 90 lines",
            "esc+0": "go up 100 lines",
            "f1": "go down 10 lines",
            "f2": "go down 20 lines",
            "f3": "go down 30 lines",
            "f4": "go down 40 lines",
            "f5": "go down 50 lines",
            "f6": "go down 60 lines",
            "f7": "go down 70 lines",
            "f8": "go down 80 lines",
            "f9": "go down 90 lines",
            "f10": "go down 100 lines",
            "ctrl+u": f"go up '{config.terminalEditorScrollLineCount}' lines [configurable]",
            "ctrl+j": f"go down '{config.terminalEditorScrollLineCount}' lines [configurable]",
        }
        keyHelp = f"{config.divider}\n\n"
        keyHelp += "# Key Bindings\n"
        keyHelp += "[blank]: launch action menu\n"
        for key, value in bindings.items():
            keyHelp += f"{key}: {value}\n"
        keyHelp += "\n## Key Bindings\n[for multiline entry only]\n"
        for key, value in multilineBindings.items():
            keyHelp += f"{key}: {value}\n"
        keyHelp += f"\n{config.divider}\n\n"
        keyHelp += config.actionHelp
        keyHelp += f"\n{config.divider}\n"

        if SharedUtil.isPackageInstalled("less"):
            pydoc.pipepager(f"To close this help page, press 'q'\n\n{keyHelp}\nTo close this help page, press 'q'", cmd='less -R')
        else:
            print(keyHelp)

    def simplePrompt(self, numberOnly=False, validator=None, inputIndicator="", default="", accept_default=False, completer=None, promptSession=None, style=None, is_password=False, bottom_toolbar=None):
        config.selectAll = False
        inputPrompt = promptSession.prompt if promptSession is not None else prompt
        if not inputIndicator:
            inputIndicator = self.inputIndicator
        if numberOnly:
            validator = NumberValidator()
        userInput = inputPrompt(
            inputIndicator,
            key_bindings=self.prompt_shared_key_bindings,
            bottom_toolbar=self.getToolBar(config.multilineInput) if bottom_toolbar is None else bottom_toolbar,
            #enable_system_prompt=True,
            swap_light_and_dark_colors=Condition(lambda: not config.terminalResourceLinkColor.startswith("ansibright")),
            style=self.promptStyle1 if style is None else style,
            validator=validator,
            multiline=Condition(lambda: config.multilineInput),
            default=default,
            accept_default=accept_default,
            completer=completer,
            is_password=is_password,
            mouse_support=Condition(lambda: config.mouseSupport),
            clipboard=config.clipboard,
        )
        userInput = textwrap.dedent(userInput) # dedent to work with code block
        return userInput if hasattr(config, "addPathAt") and config.addPathAt else userInput.strip()
