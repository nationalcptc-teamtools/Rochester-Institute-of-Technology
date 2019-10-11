using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Text.RegularExpressions;

namespace FilesystemGen
{
    class Program
    {
        static void DumpDirectory(StreamWriter outputFile, string path)
        {
            try
            {
                string[] directories = Directory.GetDirectories(path);
                string[] files = Directory.GetFiles(path);

                foreach (string directory in directories)
                {
                    DumpDirectory(outputFile, directory);
                }

                foreach (string file in files)
                {
                    outputFile.WriteLine(Regex.Replace(file, @"[^\u0000-\u007F]+", string.Empty));
                }
            } catch (Exception e)
            {
                Console.WriteLine("Swallowed exception " + e.ToString());
            }
        }
        static void Main(string[] args)
        {
            if(args.Length < 2)
            {
                Console.WriteLine("Usage:");
                Console.WriteLine("FilesystemGen.exe [BASE PATH] [OUTPUT]");
                Console.WriteLine("\tBASE PATH = The path to start mapping at.");
                Console.WriteLine("\tOUTPUT = The path to the output logs.");
                Console.ReadLine();
                return;
            }

            string basepath = args[0];
            string outputFileName = args[1];

            Console.WriteLine("[FilesystemGen] Dumping path " + basepath + ".");

            StreamWriter outputFile = File.AppendText(outputFileName);
            DumpDirectory(outputFile, basepath);
            outputFile.Close();

            Console.WriteLine("[FilesystemGen] Dumped to " + outputFileName + ".");
            Console.ReadLine();
        }
    }
}
