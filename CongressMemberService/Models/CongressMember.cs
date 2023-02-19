using Common.Enums;

namespace CongressMemberService.Models
{
    public class CongressMember
    {
        public Guid Id { get; set; }

        public string? FirstName { get; set; }

        public string? MiddleName { get; set; }

        public string? LastName { get; set; }

        public string? Gender { get; set; }

        public string? Party {get; set; }

        public string? State { get; set; }

        public string? TwitterAccountName { get; set; }

        public Chamber Chamber { get; set; }
    }
}