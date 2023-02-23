using System.ComponentModel.DataAnnotations.Schema;
using Common.Enums;

namespace Common.Models
{
    public class CongressMember
    {
        [DatabaseGenerated(DatabaseGeneratedOption.None)]
        public string ID { get; set; } = null!;
        public string? FirstName { get; set; }
        public string? LastName { get; set; }
        public string? Gender { get; set; }
        public string? Party {get; set; }
        public string? State { get; set; }
        public string? TwitterAccountName { get; set; }
        public Chamber Chamber { get; set; }
        public string? MiddleName { get; set; }
    }
}