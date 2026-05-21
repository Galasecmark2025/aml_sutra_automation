namespace python_runnner
{
    partial class Script_form
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.btnRun = new System.Windows.Forms.Button();
            this.txtScriptPath = new System.Windows.Forms.TextBox();
            this.lblExePath = new System.Windows.Forms.Label();
            this.lblStatus = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // btnRun
            // 
            this.btnRun.Location = new System.Drawing.Point(490, 117);
            this.btnRun.Name = "btnRun";
            this.btnRun.Size = new System.Drawing.Size(75, 23);
            this.btnRun.TabIndex = 0;
            this.btnRun.Text = "Run";
            this.btnRun.UseVisualStyleBackColor = true;
            this.btnRun.Click += new System.EventHandler(this.btnRun_Click);
            // 
            // txtScriptPath
            // 
            this.txtScriptPath.Location = new System.Drawing.Point(170, 119);
            this.txtScriptPath.Name = "txtScriptPath";
            this.txtScriptPath.Size = new System.Drawing.Size(298, 20);
            this.txtScriptPath.TabIndex = 1;
            // 
            // lblExePath
            // 
            this.lblExePath.AutoSize = true;
            this.lblExePath.Location = new System.Drawing.Point(77, 122);
            this.lblExePath.Name = "lblExePath";
            this.lblExePath.Size = new System.Drawing.Size(87, 13);
            this.lblExePath.TabIndex = 2;
            this.lblExePath.Text = "Enter Script Path";
            // 
            // lblStatus
            // 
            this.lblStatus.AutoSize = true;
            this.lblStatus.ForeColor = System.Drawing.SystemColors.MenuHighlight;
            this.lblStatus.Location = new System.Drawing.Point(278, 178);
            this.lblStatus.Name = "lblStatus";
            this.lblStatus.Size = new System.Drawing.Size(173, 13);
            this.lblStatus.TabIndex = 3;
            this.lblStatus.Text = "Please wait... Automation is starting";
            this.lblStatus.Visible = false;
            // 
            // Script_form
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Controls.Add(this.lblStatus);
            this.Controls.Add(this.lblExePath);
            this.Controls.Add(this.txtScriptPath);
            this.Controls.Add(this.btnRun);
            this.Name = "Script_form";
            this.Text = "Script_form";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button btnRun;
        private System.Windows.Forms.TextBox txtScriptPath;
        private System.Windows.Forms.Label lblExePath;
        private System.Windows.Forms.Label lblStatus;
    }
}

