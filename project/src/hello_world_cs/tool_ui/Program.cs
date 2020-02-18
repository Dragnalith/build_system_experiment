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
            WpfApplication1.App app = new WpfApplication1.App();
            app.InitializeComponent();
            app.Run();
        }
    }
}