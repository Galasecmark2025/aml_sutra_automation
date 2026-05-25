namespace script_runner
{
    partial class Script_Writer_Form
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
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
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            lblMain_Menu = new Label();
            tbMain_Menu = new TextBox();
            lblSubMenu = new Label();
            tbSubMenu = new TextBox();
            lblcompany = new Label();
            tbcompany = new TextBox();
            lblprocesstype = new Label();
            tbprocesstype = new TextBox();
            lblprocessids = new Label();
            tbprocessids = new TextBox();
            lbldate = new Label();
            dtpdate = new DateTimePicker();
            rtbjson = new RichTextBox();
            lbljson = new Label();
            lblTitle = new Label();
            lblSubtile = new Label();
            lblReset = new Button();
            btnStart = new Button();
            lbljsondescription = new Label();
            SuspendLayout();
            // 
            // lblMain_Menu
            // 
            lblMain_Menu.AutoSize = true;
            lblMain_Menu.ForeColor = Color.FromArgb(30, 41, 59);
            lblMain_Menu.Location = new Point(83, 95);
            lblMain_Menu.Name = "lblMain_Menu";
            lblMain_Menu.Size = new Size(80, 19);
            lblMain_Menu.TabIndex = 0;
            lblMain_Menu.Text = "Main Menu";
            // 
            // tbMain_Menu
            // 
            tbMain_Menu.BackColor = Color.White;
            tbMain_Menu.BorderStyle = BorderStyle.FixedSingle;
            tbMain_Menu.Location = new Point(66, 117);
            tbMain_Menu.Name = "tbMain_Menu";
            tbMain_Menu.Size = new Size(220, 25);
            tbMain_Menu.TabIndex = 1;
            // 
            // lblSubMenu
            // 
            lblSubMenu.AutoSize = true;
            lblSubMenu.Location = new Point(303, 95);
            lblSubMenu.Name = "lblSubMenu";
            lblSubMenu.Size = new Size(72, 19);
            lblSubMenu.TabIndex = 2;
            lblSubMenu.Text = "Sub Menu";
            // 
            // tbSubMenu
            // 
            tbSubMenu.BackColor = Color.White;
            tbSubMenu.BorderStyle = BorderStyle.FixedSingle;
            tbSubMenu.Location = new Point(292, 117);
            tbSubMenu.Name = "tbSubMenu";
            tbSubMenu.Size = new Size(220, 25);
            tbSubMenu.TabIndex = 3;
            // 
            // lblcompany
            // 
            lblcompany.AutoSize = true;
            lblcompany.Location = new Point(531, 95);
            lblcompany.Name = "lblcompany";
            lblcompany.Size = new Size(68, 19);
            lblcompany.TabIndex = 4;
            lblcompany.Text = "Company";
            // 
            // tbcompany
            // 
            tbcompany.BackColor = Color.White;
            tbcompany.BorderStyle = BorderStyle.FixedSingle;
            tbcompany.Location = new Point(518, 117);
            tbcompany.Name = "tbcompany";
            tbcompany.Size = new Size(220, 25);
            tbcompany.TabIndex = 5;
            // 
            // lblprocesstype
            // 
            lblprocesstype.AutoSize = true;
            lblprocesstype.Location = new Point(761, 95);
            lblprocesstype.Name = "lblprocesstype";
            lblprocesstype.Size = new Size(87, 19);
            lblprocesstype.TabIndex = 6;
            lblprocesstype.Text = "Process Type";
            // 
            // tbprocesstype
            // 
            tbprocesstype.BackColor = Color.White;
            tbprocesstype.BorderStyle = BorderStyle.FixedSingle;
            tbprocesstype.Location = new Point(744, 117);
            tbprocesstype.Name = "tbprocesstype";
            tbprocesstype.Size = new Size(220, 25);
            tbprocesstype.TabIndex = 7;
            // 
            // lblprocessids
            // 
            lblprocessids.AutoSize = true;
            lblprocessids.Location = new Point(83, 174);
            lblprocessids.Name = "lblprocessids";
            lblprocessids.Size = new Size(77, 19);
            lblprocessids.TabIndex = 8;
            lblprocessids.Text = "Process Ids";
            // 
            // tbprocessids
            // 
            tbprocessids.BackColor = Color.White;
            tbprocessids.BorderStyle = BorderStyle.FixedSingle;
            tbprocessids.Location = new Point(66, 196);
            tbprocessids.Name = "tbprocessids";
            tbprocessids.Size = new Size(443, 25);
            tbprocessids.TabIndex = 9;
            // 
            // lbldate
            // 
            lbldate.AutoSize = true;
            lbldate.Location = new Point(531, 174);
            lbldate.Name = "lbldate";
            lbldate.Size = new Size(38, 19);
            lbldate.TabIndex = 10;
            lbldate.Text = "Date";
            // 
            // dtpdate
            // 
            dtpdate.Location = new Point(515, 196);
            dtpdate.Name = "dtpdate";
            dtpdate.Size = new Size(147, 25);
            dtpdate.TabIndex = 11;
            // 
            // rtbjson
            // 
            rtbjson.BackColor = Color.White;
            rtbjson.BorderStyle = BorderStyle.FixedSingle;
            rtbjson.Font = new Font("Consolas", 10F);
            rtbjson.Location = new Point(66, 288);
            rtbjson.Name = "rtbjson";
            rtbjson.Size = new Size(895, 202);
            rtbjson.TabIndex = 12;
            rtbjson.Text = "";
            // 
            // lbljson
            // 
            lbljson.AutoSize = true;
            lbljson.Font = new Font("Segoe UI", 12F);
            lbljson.Location = new Point(83, 247);
            lbljson.Name = "lbljson";
            lbljson.Size = new Size(49, 21);
            lbljson.TabIndex = 13;
            lbljson.Text = "JSON";
            // 
            // lblTitle
            // 
            lblTitle.AutoSize = true;
            lblTitle.Font = new Font("Segoe UI", 18F);
            lblTitle.Location = new Point(40, 30);
            lblTitle.Name = "lblTitle";
            lblTitle.Size = new Size(247, 32);
            lblTitle.TabIndex = 14;
            lblTitle.Text = "Process Configuration";
            // 
            // lblSubtile
            // 
            lblSubtile.AutoSize = true;
            lblSubtile.ForeColor = Color.Gray;
            lblSubtile.Location = new Point(42, 70);
            lblSubtile.Name = "lblSubtile";
            lblSubtile.Size = new Size(303, 19);
            lblSubtile.TabIndex = 15;
            lblSubtile.Text = "Enter the details below to configure the process.";
            // 
            // lblReset
            // 
            lblReset.BackColor = Color.White;
            lblReset.Location = new Point(688, 525);
            lblReset.Name = "lblReset";
            lblReset.Size = new Size(120, 40);
            lblReset.TabIndex = 16;
            lblReset.Text = "Reset";
            lblReset.UseVisualStyleBackColor = false;
            // 
            // btnStart
            // 
            btnStart.BackColor = Color.FromArgb(37, 99, 235);
            btnStart.FlatStyle = FlatStyle.Flat;
            btnStart.ForeColor = Color.White;
            btnStart.Location = new Point(844, 525);
            btnStart.Name = "btnStart";
            btnStart.Size = new Size(120, 40);
            btnStart.TabIndex = 17;
            btnStart.Text = "Start";
            btnStart.UseVisualStyleBackColor = false;
            btnStart.Click += btnStart_Click;
            // 
            // lbljsondescription
            // 
            lbljsondescription.AutoSize = true;
            lbljsondescription.ForeColor = Color.Gray;
            lbljsondescription.Location = new Point(83, 266);
            lbljsondescription.Name = "lbljsondescription";
            lbljsondescription.Size = new Size(221, 19);
            lbljsondescription.TabIndex = 18;
            lbljsondescription.Text = "Provide JSON data for the process.";
            // 
            // Script_Writer_Form
            // 
            AutoScaleDimensions = new SizeF(7F, 17F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.FromArgb(245, 247, 250);
            ClientSize = new Size(1033, 623);
            Controls.Add(lbljsondescription);
            Controls.Add(btnStart);
            Controls.Add(lblReset);
            Controls.Add(lblSubtile);
            Controls.Add(lblTitle);
            Controls.Add(lbljson);
            Controls.Add(rtbjson);
            Controls.Add(dtpdate);
            Controls.Add(lbldate);
            Controls.Add(tbprocessids);
            Controls.Add(lblprocessids);
            Controls.Add(tbprocesstype);
            Controls.Add(lblprocesstype);
            Controls.Add(tbcompany);
            Controls.Add(lblcompany);
            Controls.Add(tbSubMenu);
            Controls.Add(lblSubMenu);
            Controls.Add(tbMain_Menu);
            Controls.Add(lblMain_Menu);
            Font = new Font("Segoe UI", 10F);
            ForeColor = SystemColors.ControlText;
            Name = "Script_Writer_Form";
            StartPosition = FormStartPosition.CenterScreen;
            Text = " Process Configuration";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Label lblMain_Menu;
        private TextBox tbMain_Menu;
        private Label lblSubMenu;
        private TextBox tbSubMenu;
        private Label lblcompany;
        private TextBox tbcompany;
        private Label lblprocesstype;
        private TextBox tbprocesstype;
        private Label lblprocessids;
        private TextBox tbprocessids;
        private Label lbldate;
        private DateTimePicker dtpdate;
        private RichTextBox rtbjson;
        private Label lbljson;
        private Label lblTitle;
        private Label lblSubtile;
        private Button lblReset;
        private Button btnStart;
        private Label lbljsondescription;
    }
}
