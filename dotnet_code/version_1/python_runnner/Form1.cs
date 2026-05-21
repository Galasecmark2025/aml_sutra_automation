using System;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Windows.Forms;

namespace python_runnner
{
    public partial class Script_form : Form
    {
        public Script_form()
        {
            InitializeComponent();
        }

        private async void btnRun_Click(object sender, EventArgs e)
        {
            try
            {
                // SHOW LOADING MESSAGE
                lblStatus.Text =
                    "Please wait... Automation is starting";

                lblStatus.Visible = true;

                Application.DoEvents();

                // PYTHON EXE PATH
                string pythonExe =
                    @"C:\Users\visha\AppData\Local\Python\pythoncore-3.14-64\python.exe";

                // SCRIPT PATH
                string scriptPath = txtScriptPath.Text.Trim();

                // VALIDATION
                if (string.IsNullOrEmpty(scriptPath))
                {
                    lblStatus.Visible = false;

                    MessageBox.Show(
                        "Please enter Python script path"
                    );

                    return;
                }

                // FILE EXISTS CHECK
                if (!File.Exists(scriptPath))
                {
                    lblStatus.Visible = false;

                    MessageBox.Show(
                        "Python script file not found"
                    );

                    return;
                }

                // PROCESS SETTINGS
                ProcessStartInfo psi = new ProcessStartInfo()
                {
                    FileName = pythonExe,

                    Arguments = $"\"{scriptPath}\"",

                    UseShellExecute = false,

                    RedirectStandardOutput = true,

                    RedirectStandardError = true,

                    CreateNoWindow = true,

                    WorkingDirectory =
                        Path.GetDirectoryName(scriptPath)
                };

                // PROCESS OBJECT
                Process process = new Process();

                process.StartInfo = psi;

                process.EnableRaisingEvents = true;

                StringBuilder output =
                    new StringBuilder();

                StringBuilder error =
                    new StringBuilder();

                // OUTPUT EVENT
                process.OutputDataReceived += (s, ev) =>
                {
                    if (!string.IsNullOrEmpty(ev.Data))
                    {
                        output.AppendLine(ev.Data);
                    }
                };

                // ERROR EVENT
                process.ErrorDataReceived += (s, ev) =>
                {
                    if (!string.IsNullOrEmpty(ev.Data))
                    {
                        error.AppendLine(ev.Data);
                    }
                };

                // START PROCESS
                process.Start();


                // BEGIN ASYNC READ
                process.BeginOutputReadLine();

                process.BeginErrorReadLine();

                // WAIT WITHOUT FREEZING UI
                await System.Threading.Tasks.Task.Run(() =>
                {
                    process.WaitForExit();
                });

                // HIDE LOADING MESSAGE
                lblStatus.Visible = false;

                // FINAL MESSAGE
                if (process.ExitCode == 0)
                {
                    MessageBox.Show(
                        "Automation completed successfully.",
                        "Success",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Information
                    );
                }
                else
                {
                    MessageBox.Show(
                        "Automation completed with errors.\n\n" +
                        error.ToString(),
                        "Error",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Error
                    );
                }
            }
            catch (Exception ex)
            {
                lblStatus.Visible = false;

                MessageBox.Show(
                    ex.ToString(),
                    "Exception",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error
                );
            }
        }
    }
}