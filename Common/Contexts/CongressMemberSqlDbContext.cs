using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Common.Models;

namespace Common.Contexts
{
    public class CongressMemberSqlDbContext : DbContext, ICongressMemberDbContext
    {
        public DbSet<CongressMember> CongressMembers { get; set; } = null!;
        private readonly IConfiguration _configuration;

        public CongressMemberSqlDbContext(
            DbContextOptions<CongressMemberSqlDbContext> options,
            IConfiguration configuration) : base(options)
        {
            _configuration = configuration;

            // to prevent errors on first run with empty tables
            Database.EnsureCreated();
        }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            // configure to use SQL server
            optionsBuilder.UseSqlServer(_configuration.GetConnectionString("CongressMemberDb"));
        }
    }
}