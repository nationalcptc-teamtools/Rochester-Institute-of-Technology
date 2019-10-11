using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Text.RegularExpressions;

namespace FilesystemAnalyze
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length < 3)
            {
                Console.WriteLine("Usage:");
                Console.WriteLine("FilesystemAnalyze.exe [BASELINE] [LIVE MACHINE] [OUTPUT]");
                Console.WriteLine("\tBASELINE = The path to the baseline file.");
                Console.WriteLine("\tLIVE MACHINE = The path to the results of a live machine.");
                Console.WriteLine("\tOUTPUT = Filename for results.");
                Console.ReadLine();
                return;
            }

            Console.WriteLine("[FilesystemAnalyze] Reading in baseline file " + args[0] + ".");
            string[] importedBaselineFiles = File.ReadAllLines(args[0]);

            Console.WriteLine("[FilesystemAnalyze] Sorting in baseline file " + args[0] + ".");
            Array.Sort(importedBaselineFiles, StringComparer.InvariantCulture);

            Console.WriteLine("[FilesystemAnalyze] Reading in live machine file " + args[1] + ".");
            string[] importedLiveFiles = File.ReadAllLines(args[1]);

            Console.WriteLine("[FilesystemAnalyze] Beginning single-threaded search, results will be stored at " + args[2] + ".");
            StreamWriter outputFile = File.AppendText(args[2]);

            foreach(string livepath in importedLiveFiles)
            {
                if(Array.BinarySearch(importedBaselineFiles, Regex.Replace(livepath, @"[^\u0000-\u007F]+", string.Empty)) < 0)
                {
                    outputFile.WriteLine(livepath);
                }
            }

            outputFile.Close();

            Console.WriteLine("[FilesystemAnalyze] Finished dumping.");
            Console.ReadLine();
        }
    }
}
