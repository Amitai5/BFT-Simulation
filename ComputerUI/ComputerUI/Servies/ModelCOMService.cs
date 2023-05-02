using System.IO.Ports;

namespace ComputerUI.Servies
{
    public class ModelCOMService
    {
        public const int COMReadTimeoutMS = 1500;
        public const string ModelID = "BT-1826";

        public bool IsConnected { get; private set; } = false;
        public event ConnectionEvent OnConnected;
        public delegate void ConnectionEvent();

        public delegate void DataRecievedEvent(double force);
        public event DataRecievedEvent DataReceived;
        private SerialPort ModelCOMPort;

        public ModelCOMService()
        {

        }

        private void ModelCOMPort_DataReceived(object sender, SerialDataReceivedEventArgs e)
        {
            string data = ModelCOMPort.ReadLine();
            if (data.StartsWith(">>"))
            {
                data = data[2..].Trim(); // Remove the '>>'
                double force = double.Parse(data[..data.IndexOf(';')]);
                DataReceived?.Invoke(force);
            }
        }

        public void ConnectToModel()
        {
            Thread thread = new(() => connectToModel());
            thread.Start();
        }

        private void connectToModel()
        {
            string[] comPorts = SerialPort.GetPortNames();
            foreach (string comPort in comPorts)
            {
                SerialPort port = new SerialPort(comPort)
                {
                    DtrEnable = true,
                    RtsEnable = true,
                    BaudRate = 9600
                };

                if (checkPort(port) == true)
                {
                    ModelCOMPort = port;
                    IsConnected = true;
                    break;
                }
            }

            if (ModelCOMPort == null)
            {
                // TODO: Send error message
                return;
            }

            // Tell the model we have recieved its message
            ModelCOMPort.WriteLine(ModelID);
            Thread.Sleep(COMReadTimeoutMS);

            // Raise the event and also subscribe to the data recieved event
            ModelCOMPort.DataReceived += ModelCOMPort_DataReceived;
            OnConnected?.Invoke();
        }

        private bool checkPort(SerialPort port)
        {
            // Allow only 2 seconds to read the port for data
            port.ReadTimeout = COMReadTimeoutMS;

            try
            {
                port.Open();
                string data = port.ReadLine();
                return data.Trim().Contains(ModelID);
            }
            catch
            {
                if (port.IsOpen)
                {
                    port.Close();
                }

                port.Dispose();
            }
            return false;
        }
    }
}
