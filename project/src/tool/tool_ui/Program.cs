using System;
using System.Diagnostics;

namespace WpfApplication1
{
    public partial class App : System.Windows.Application
    {

        public void InitializeComponent()
        {
            this.StartupUri = new System.Uri("MainWindow.xaml", System.UriKind.Relative);
        }

        [System.STAThreadAttribute()]
        public static void Main()
        {
            System.Console.Write("Hellooooo World\n");
            string[] resourceNames = typeof(App).Assembly.GetManifestResourceNames();
            foreach(string resourceName in resourceNames)
            {
                System.Console.WriteLine(resourceName);
            }  
            WpfApplication1.App app = new WpfApplication1.App();
            app.InitializeComponent();
            app.Run();
        }
    }
}