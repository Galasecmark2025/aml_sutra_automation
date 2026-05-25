using Newtonsoft.Json;
using System.Diagnostics;
using System.IO;

namespace script_runner
{
    public partial class Script_Writer_Form : Form
    {
        public Script_Writer_Form()
        {
            InitializeComponent();
        }

        private void btnStart_Click(object sender, EventArgs e)
        {
            try
            {
                btnStart.Enabled = false;

                string jsonText = "";

                // USE MANUAL JSON IF EXISTS
                if (!string.IsNullOrWhiteSpace(rtbjson.Text))
                {
                    jsonText = rtbjson.Text;
                }
                else
                {
                    // AUTO CREATE JSON

                    var jsonObject = new
                    {
                        main_menu = tbMain_Menu.Text,

                        sub_menu = tbSubMenu.Text,

                        company = tbcompany.Text,

                        proc_type = tbprocesstype.Text,

                        proc_ids = tbprocessids.Text
                            .Split(',')
                            .Select(x => Convert.ToInt32(x.Trim()))
                            .ToArray(),

                        date = dtpdate.Value
                            .ToString("dd-MMM-yyyy")
                    };

                    jsonText = JsonConvert.SerializeObject(
                        jsonObject,
                        Formatting.Indented
                    );

                    // SHOW GENERATED JSON
                    rtbjson.Text = jsonText;
                }

                // SAVE TEMP JSON

                string jsonPath = Path.Combine(
                    Application.StartupPath,
                    "process.json"
                );

                File.WriteAllText(jsonPath, jsonText);

                // RUN PYTHON
                RunPython();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
            finally
            {
                btnStart.Enabled = true;
            }
        }

private void RunPython()
{
    try
    {
                ProcessStartInfo psi = new ProcessStartInfo();

                // PYTHON
                psi.FileName = "python";

                // SCRIPT NAME ONLY
                psi.Arguments = "app_v5.py";

                // PYTHON FOLDER
                psi.WorkingDirectory =
                    @"D:\python_scripts\aml_sutra_automation";

                // SHOW PYTHON CONSOLE
                psi.UseShellExecute = true;

                psi.CreateNoWindow = false;

                // DEBUG
                MessageBox.Show(
                    psi.FileName + " " +
                    psi.Arguments +
                    "\n\nWorking Directory:\n" +
                    psi.WorkingDirectory
                );

                Process process = new Process();

                process.StartInfo = psi;

                process.Start();

                string output =
            process.StandardOutput.ReadToEnd();

        string error =
            process.StandardError.ReadToEnd();

        process.WaitForExit();

        // SHOW OUTPUT
        if (!string.IsNullOrWhiteSpace(error))
        {
            MessageBox.Show(
                "ERROR:\n\n" + error
            );
        }
        else
        {
            MessageBox.Show(
                "OUTPUT:\n\n" + output
            );
        }
    }
    catch (Exception ex)
    {
        MessageBox.Show(ex.Message);
    }
}

    }
}
