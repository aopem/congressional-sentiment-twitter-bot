using Common.Enums;

namespace Common.Models
{
    public class CongressMember
    {
        public int ID { get; set; }
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public string Gender { get; set; }
        public string Party {get; set; }
        public string State { get; set; }
        public string TwitterAccountName { get; set; }
        public Chamber Chamber { get; set; }
        public string? MiddleName { get; set; }

        public CongressMember(
            string firstName,
            string lastName,
            string gender,
            string party,
            string state,
            string twitterAccountName,
            Chamber chamber,
            string? middleName = null)
        {
            this.FirstName = firstName;
            this.LastName = lastName;
            this.Gender = gender;
            this.Party = party;
            this.State = state;
            this.TwitterAccountName = twitterAccountName;
            this.Chamber = chamber;
            this.MiddleName = middleName;
        }
    }
}