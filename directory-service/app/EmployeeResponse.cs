using System;
using System.Collections.Generic;

namespace DirectoryService
{
    public class EmployeeResponse
    {
        public EmployeeResponse() {
            Message = $"Hello from {Environment.MachineName}";
        }

        public string Message { get; set; }

        public Employee Employee { get; set; }
    }
}
