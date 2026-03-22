// See https://aka.ms/new-console-template for more information
//Console.WriteLine("Hello, World!");

using System;
using System.Net.Sockets;
using System.Text;

class Program
{
    const string SERVER_IP = "127.0.0.1";
    const int SERVER_PORT = 9000;
    const string HASH = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824";


    static void Main()
    {
        try
        {
            using (TcpClient client = new TcpClient())
            {
                client.Connect(SERVER_IP, SERVER_PORT);
                Console.WriteLine($"Pripojené na {SERVER_IP}:{SERVER_PORT}");

                using (NetworkStream stream = client.GetStream())
                {
                      // =====================================================
                      // --- ukazka volania GET ---
                      // ======================================================
                      byte[] cmd = Encoding.UTF8.GetBytes($"GET {HASH}\n");
                      stream.Write(cmd, 0, cmd.Length);
                      // precitaj hlavičku
                      StringBuilder header = new StringBuilder();
                      while (true)
                      {
                            int b = stream.ReadByte();
                            if (b == -1 || b == '\n') break;
                            header.Append((char)b);
                      }
                      Console.WriteLine("Hlavička servera: " + header);

                      if (!header.ToString().StartsWith("200")) return;

                      // správne parsovanie: 200 OK <length> <description>
                      string[] parts = header.ToString().Split(new char[]{' '}, 4);
                      int length = int.Parse(parts[2]);
                      string description = parts[3];

                      byte[] data = new byte[length];
                      stream.Read(data, 0, length);

                      Console.WriteLine("Obsah súboru:");
                      Console.WriteLine(Encoding.UTF8.GetString(data));
                      // --- KONIEK UKAZKY ---

                      // Tu implementovat protokol dalej, moznost pisat kod lienarne alebo pouzit procesury/funkcie/metody
                }

                Console.WriteLine("Spojenie zatvorené");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Chyba: {ex.Message}");
        }
    }
}





