from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.clipboard import Clipboard
import traceback
import re
import sys
from io import StringIO

class CodeCorrector(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=8)
        
        title = Label(text='[b]AI Code Corrector v2.0[/b]\n[AI Debug | Smart Fix | Run | Save]', markup=True, size_hint_y=0.08, font_size='16sp')
        
        toolbar = BoxLayout(size_hint_y=0.07, spacing=5)
        find_btn = Button(text='AI Find')
        find_btn.bind(on_press=self.find_errors)
        fix_btn = Button(text='AI Fix')
        fix_btn.bind(on_press=self.auto_fix)
        run_btn = Button(text='Run')
        run_btn.bind(on_press=self.run_code)
        save_btn = Button(text='Save')
        save_btn.bind(on_press=self.save_file)
        load_btn = Button(text='Load')
        load_btn.bind(on_press=self.load_file)
        copy_btn = Button(text='Copy')
        copy_btn.bind(on_press=self.copy_code)
        reset_btn = Button(text='Reset')
        reset_btn.bind(on_press=self.reset_all)
        
        toolbar.add_widget(find_btn)
        toolbar.add_widget(fix_btn)
        toolbar.add_widget(run_btn)
        toolbar.add_widget(save_btn)
        toolbar.add_widget(load_btn)
        toolbar.add_widget(copy_btn)
        toolbar.add_widget(reset_btn)
        
        input_label = Label(text='--- Your Code ---', size_hint_y=0.03)
        self.input_code = TextInput(hint_text='Write or paste your Python code here...', multiline=True, size_hint_y=0.30, font_size='12sp')
        
        bottom_layout = BoxLayout(orientation='vertical', size_hint_y=0.48, spacing=5)
        tab_layout = BoxLayout(size_hint_y=0.08, spacing=5)
        
        btn1 = Button(text='[1] AI ERRORS')
        btn1.bind(on_press=self.show_errors)
        btn2 = Button(text='[2] AI FIXES')
        btn2.bind(on_press=self.show_fixes)
        btn3 = Button(text='[3] OUTPUT')
        btn3.bind(on_press=self.show_output)
        
        tab_layout.add_widget(btn1)
        tab_layout.add_widget(btn2)
        tab_layout.add_widget(btn3)
        
        self.panel_container = BoxLayout(orientation='vertical', size_hint_y=0.92)
        
        self.errors_panel = TextInput(text='', multiline=True, font_size='12sp', readonly=True)
        self.fixes_panel = TextInput(text='', multiline=True, font_size='12sp', readonly=True)
        self.output_panel = TextInput(text='', multiline=True, font_size='12sp', readonly=True)
        
        self.panel_container.add_widget(self.errors_panel)
        self.panel_container.add_widget(self.fixes_panel)
        self.panel_container.add_widget(self.output_panel)
        
        self.current_panel = 'errors'
        self.errors_panel.opacity = 1
        self.errors_panel.disabled = False
        self.fixes_panel.opacity = 0
        self.fixes_panel.disabled = True
        self.output_panel.opacity = 0
        self.output_panel.disabled = True
        
        self.display_welcome()
        
        bottom_layout.add_widget(tab_layout)
        bottom_layout.add_widget(self.panel_container)
        
        main_layout.add_widget(title)
        main_layout.add_widget(toolbar)
        main_layout.add_widget(input_label)
        main_layout.add_widget(self.input_code)
        main_layout.add_widget(bottom_layout)
        
        return main_layout
    
    def reset_all(self, instance):
        """Reset all fields"""
        self.input_code.text = ''
        self.errors_panel.text = ''
        self.fixes_panel.text = ''
        self.output_panel.text = ''
        self.display_welcome()
        self.show_errors(None)
    
    def show_errors(self, instance):
        self.errors_panel.opacity = 1
        self.errors_panel.disabled = False
        self.fixes_panel.opacity = 0
        self.fixes_panel.disabled = True
        self.output_panel.opacity = 0
        self.output_panel.disabled = True
    
    def show_fixes(self, instance):
        self.errors_panel.opacity = 0
        self.errors_panel.disabled = True
        self.fixes_panel.opacity = 1
        self.fixes_panel.disabled = False
        self.output_panel.opacity = 0
        self.output_panel.disabled = True
    
    def show_output(self, instance):
        self.errors_panel.opacity = 0
        self.errors_panel.disabled = True
        self.fixes_panel.opacity = 0
        self.fixes_panel.disabled = True
        self.output_panel.opacity = 1
        self.output_panel.disabled = False
    
    def display_welcome(self):
        welcome = "="*70 + "\n"
        welcome += " " * 15 + "AI CODE CORRECTOR v2.0\n"
        welcome += "="*70 + "\n\n"
        welcome += "[AI Algorithms Active]\n\n"
        welcome += "[1] AI ERRORS -> AI detects and classifies errors\n"
        welcome += "[2] AI FIXES  -> AI suggests intelligent fixes\n"
        welcome += "[3] OUTPUT    -> Run your code\n\n"
        welcome += "AI Features:\n"
        welcome += "- Error pattern recognition\n"
        welcome += "- Smart fix suggestions\n"
        welcome += "- Code complexity analysis\n"
        welcome += "="*70
        self.errors_panel.text = welcome
    
    def ai_classify_error(self, error_msg, error_line):
        """AI algorithm to classify error type"""
        error_lower = error_msg.lower()
        
        if 'indent' in error_lower:
            return 'INDENTATION ERROR', 'Check your spaces. Use 4 spaces for each level.'
        elif 'colon' in error_lower or 'expected' in error_lower:
            return 'MISSING COLON', 'Add ":" at the end of the line.'
        elif 'syntax' in error_lower:
            if '=' in error_lower and '==' not in error_lower:
                return 'ASSIGNMENT VS COMPARISON', 'Use "==" for comparison, not "="'
            return 'SYNTAX ERROR', 'Check the line for typos or missing symbols.'
        elif 'name' in error_lower and 'defined' in error_lower:
            return 'UNDEFINED VARIABLE', 'Define the variable before using it.'
        elif 'unexpected' in error_lower:
            return 'UNEXPECTED TOKEN', 'Check for extra or missing characters.'
        else:
            return 'GENERIC ERROR', 'Review the line carefully.'
    
    def ai_suggest_fix(self, error_msg, error_text):
        """AI algorithm to suggest fixes based on error patterns"""
        error_lower = error_msg.lower()
        suggestions = []
        
        patterns = {
            'prinnt': "Change 'prinnt' to 'print'",
            'pint': "Change 'pint' to 'print'",
            'ture': "Change 'ture' to 'True'",
            'flase': "Change 'flase' to 'False'",
            'def ': "Check if function name is valid and ends with ':'",
            'if ': "Check condition syntax and add ':' at end",
            'for ': "Check loop syntax and add ':' at end",
            'while ': "Check loop condition and add ':' at end"
        }
        
        for pattern, fix in patterns.items():
            if pattern in error_text.lower():
                suggestions.append(fix)
        
        if '=' in error_text and '==' not in error_text and 'if ' in error_text:
            suggestions.append("In 'if' statement, use '==' for comparison instead of '='")
        
        if not suggestions:
            suggestions.append("Check line for missing colons, parentheses, or quotes")
            suggestions.append("Verify variable names and indentation")
        
        return suggestions
    
    def ai_code_quality_score(self, code):
        """AI algorithm to calculate code quality score"""
        score = 100
        issues = []
        
        lines = code.split('\n')
        if len(lines) > 0:
            # Check for empty lines at end
            if lines[-1].strip() == '':
                score -= 5
                issues.append("Empty line at end of file")
        
        # Check for long lines
        for i, line in enumerate(lines):
            if len(line) > 79:
                score -= 2
                issues.append(f"Line {i+1} is too long ({len(line)} chars)")
        
        # Check for missing docstring in functions
        if 'def ' in code and ('"""' not in code and "'''" not in code):
            score -= 10
            issues.append("Functions should have docstrings")
        
        # Check for unused imports
        import_lines = [l for l in lines if l.startswith('import ') or l.startswith('from ')]
        if len(import_lines) > 3:
            score -= 3
            issues.append("Too many imports, consider organizing them")
        
        return max(0, score), issues
    
    def find_errors(self, instance):
        code = self.input_code.text
        if not code.strip():
            self.errors_panel.text = "="*70 + "\n[AI] NO CODE\n\nPlease write or paste some Python code first.\n" + "="*70
            return
        
        # AI Quality Score
        quality_score, quality_issues = self.ai_code_quality_score(code)
        
        try:
            compile(code, '<string>', 'exec')
            result = "="*70 + "\n"
            result += "[AI ANALYSIS] NO SYNTAX ERRORS\n\n"
            result += f"Code Quality Score: {quality_score}/100\n\n"
            if quality_issues:
                result += "Quality suggestions:\n"
                for issue in quality_issues[:3]:
                    result += f"  - {issue}\n"
            result += "\n" + "="*70
            self.errors_panel.text = result
        except SyntaxError as e:
            error_type, advice = self.ai_classify_error(str(e), e.lineno)
            
            result = "="*70 + "\n"
            result += "[AI ERROR DETECTION]\n\n"
            result += f"Error Type: {error_type}\n"
            result += f"Line: {e.lineno}\n"
            result += f"Message: {str(e).replace('(code string)', '').strip()}\n\n"
            if e.text:
                result += f"Code: {e.text.rstrip()}\n"
                if e.offset:
                    result += " " * (e.offset + 5) + "^\n"
            result += f"\nAI Advice: {advice}\n"
            result += "="*70
            self.errors_panel.text = result
        
        self.show_errors(None)
    
    def auto_fix(self, instance):
        code = self.input_code.text
        if not code.strip():
            self.fixes_panel.text = "="*70 + "\n[AI] NO CODE\n\nPlease write or paste some Python code first.\n" + "="*70
            self.show_fixes(None)
            return
        
        lines = code.split('\n')
        new_lines = []
        fixes = []
        
        for i, line in enumerate(lines):
            line_num = i + 1
            original = line
            
            # AI Pattern-based fixes
            match = re.match(r'^(\s*)(if|for|while|def|elif|else)\s+(.+?)(\s*)$', line)
            if match and not line.rstrip().endswith(':'):
                indent, keyword, condition, trailing = match.groups()
                line = f"{indent}{keyword} {condition}:"
                fixes.append(f"Line {line_num}: AI added missing ':'")
            
            if 'if ' in line and '=' in line and '==' not in line:
                new_line = re.sub(r'if\s+(\w+)\s*=\s*([^:]+)', r'if \1 == \2', line)
                if new_line != line:
                    line = new_line
                    fixes.append(f"Line {line_num}: AI changed '=' to '=='")
            
            typo_fixes = {
                'prinnt': 'print',
                'pint': 'print',
                'ture': 'True',
                'flase': 'False',
                'flse': 'False',
                'tru': 'True'
            }
            for typo, correct in typo_fixes.items():
                if typo in line:
                    line = line.replace(typo, correct)
                    fixes.append(f"Line {line_num}: AI fixed '{typo}' -> '{correct}'")
            
            # Call ai_suggest_fix for additional suggestions
            if line != original:
                suggestions = self.ai_suggest_fix("", original)
                for s in suggestions[:1]:
                    if s not in str(fixes):
                        fixes.append(f"Line {line_num}: {s}")
            
            new_lines.append(line)
        
        corrected = '\n'.join(new_lines)
        
        if fixes:
            result = "="*70 + "\n[AI SMART FIX SUMMARY]\n\n"
            result += "\n".join(fixes)
            result += f"\n\nTotal AI fixes: {len(fixes)}\n"
            result += "\nAI Confidence: High\n"
            result += "="*70
            self.input_code.text = corrected
        else:
            result = "="*70 + "\n[AI ANALYSIS] NO FIXES NEEDED\n\n"
            
            # AI Suggest improvements
            if 'if' in code and 'elif' not in code and code.count('if') > 2:
                result += "AI Suggestion: Consider using 'elif' for multiple conditions\n\n"
            
            if len(code.split('\n')) > 20:
                result += "AI Suggestion: Consider breaking this code into functions\n\n"
            
            result += "Your code looks syntactically correct.\n"
            result += "="*70
        
        self.fixes_panel.text = result
        self.show_fixes(None)
    
    def run_code(self, instance):
        code = self.input_code.text
        if not code.strip():
            self.output_panel.text = "="*70 + "\n[!] NO CODE\n\nPlease write or paste some Python code first.\n" + "="*70
            self.show_output(None)
            return
        
        old_stdout = sys.stdout
        redirected = StringIO()
        sys.stdout = redirected
        
        try:
            exec_globals = {}
            exec(code, exec_globals)
            output = redirected.getvalue()
            
            result = "="*70 + "\n[EXECUTION SUCCESS]\n\n"
            if output:
                result += output
            else:
                result += "Code executed successfully (no output)"
            result += "\n" + "="*70
            self.output_panel.text = result
        except Exception as e:
            result = "="*70 + "\n[RUNTIME ERROR]\n\n"
            result += traceback.format_exc()
            result += "\n" + "="*70
            self.output_panel.text = result
        finally:
            sys.stdout = old_stdout
            self.show_output(None)
    
    def save_file(self, instance):
        content = self.input_code.text
        if not content.strip():
            self.show_popup("Error", "No code to save!")
            return
        
        try:
            path = '/storage/emulated/0/Download/'
            filename = 'ai_code_corrector_output.py'
            full_path = path + filename
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.show_popup("Saved", f"File saved to:\n{full_path}")
        except Exception as e:
            self.show_popup("Error", f"Save failed:\n{str(e)}")
    
    def load_file(self, instance):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text='Enter full path to .py file:', size_hint_y=0.15))
        path_input = TextInput(hint_text='/storage/emulated/0/Download/myfile.py', text='/storage/emulated/0/Download/', multiline=False, size_hint_y=0.15)
        result_label = Label(text='', size_hint_y=0.3, font_size='11sp')
        
        def do_load(btn):
            filepath = path_input.text.strip()
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.input_code.text = f.read()
                result_label.text = f'[OK] Loaded: {filepath.split("/")[-1]}'
            except Exception as e:
                result_label.text = f'[ERROR] {str(e)[:80]}'
        
        load_btn = Button(text='LOAD FILE', size_hint_y=0.12)
        load_btn.bind(on_press=do_load)
        close_btn = Button(text='CLOSE', size_hint_y=0.12)
        
        layout.add_widget(path_input)
        layout.add_widget(load_btn)
        layout.add_widget(result_label)
        layout.add_widget(close_btn)
        
        popup = Popup(title='Load Python File', content=layout, size_hint=(0.9, 0.5))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def copy_code(self, instance):
        Clipboard.copy(self.input_code.text)
        self.show_popup("Copied", "Code copied to clipboard!")
    
    def show_popup(self, title, message):
        layout = BoxLayout(orientation='vertical', padding=10)
        layout.add_widget(Label(text=message, size_hint_y=0.8))
        btn = Button(text='OK', size_hint_y=0.2)
        popup = Popup(title=title, content=layout, size_hint=(0.7, 0.3))
        btn.bind(on_press=popup.dismiss)
        layout.add_widget(btn)
        popup.open()

if __name__ == '__main__':
    CodeCorrector().run()