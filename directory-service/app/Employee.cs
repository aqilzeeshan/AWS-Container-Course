using System;
using System.Collections.Generic;

namespace DirectoryService
{
    public class Employee
    {
        public string Id { get; set; }
        public string Fullname { get; set; }
        public string JobTitle { get; set; }
        public string Location { get; set; }
        public List<string> Badges { get; set; }

    }
}
