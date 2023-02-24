using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Newtonsoft.Json;
using Common.Models;
using CongressMemberAPI.Services;

namespace CongressMemberAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class CongressMemberController : ControllerBase
    {
        private readonly ILogger<CongressMemberController> _logger;
        private readonly CongressMemberService _congressMemberService;

        public CongressMemberController(
            ILogger<CongressMemberController> logger,
            CongressMemberService congressMemberService)
        {
            _logger = logger;
            _congressMemberService = congressMemberService;
        }

        [HttpPost]
        [ProducesResponseType(typeof(CongressMember), StatusCodes.Status201Created)]
        public async ValueTask<IActionResult> CreateOrUpdateAsync(CongressMember congressMember)
        {
            _logger.LogInformation($"[POST Request] {JsonConvert.SerializeObject(congressMember)}");

            var updatedCongressMember = new CongressMember();
            try
            {
                updatedCongressMember = await _congressMemberService.CreateCongressMemberAsync(congressMember);
            }
            catch (DbUpdateException e)
            {
                _logger.LogWarning(e.ToString());
                return Conflict(e.ToString());
            }
            catch (Exception e)
            {
                _logger.LogError(e.ToString());
                return StatusCode(StatusCodes.Status500InternalServerError, e.ToString());
            }

            _logger.LogInformation($"Request successful, returning: {JsonConvert.SerializeObject(updatedCongressMember)}");
            return CreatedAtAction(nameof(GetAsync), new { id = updatedCongressMember.ID }, updatedCongressMember);
        }

        [HttpGet("{id}")]
        [ProducesResponseType(typeof(CongressMember), StatusCodes.Status200OK)]
        public async ValueTask<IActionResult> GetAsync(string id)
        {
            _logger.LogInformation($"[GET Request] id = {id}");

            CongressMember? congressMember = null;
            try
            {
                congressMember = await _congressMemberService.RetrieveCongressMemberAsync(id);
            }
            catch (Exception e)
            {
                _logger.LogError(e.ToString());
                return StatusCode(StatusCodes.Status500InternalServerError, e.Message);
            }

            if (congressMember is null)
            {
                return NotFound();
            }

            _logger.LogInformation($"Request successful, returning: {JsonConvert.SerializeObject(congressMember)}");
            return Ok(congressMember);
        }

        [HttpGet]
        [ProducesResponseType(typeof(IQueryable<CongressMember>), StatusCodes.Status200OK)]
        public IActionResult GetAll()
        {
            _logger.LogInformation("[GET Request] id = all");

            IQueryable<CongressMember>? congressMembers = null;
            try
            {
                congressMembers = _congressMemberService.RetrieveAllCongressMembers();
            }
            catch (Exception e)
            {
                _logger.LogError(e.ToString());
                return StatusCode(StatusCodes.Status500InternalServerError, e.ToString());
            }

            if (congressMembers is null)
            {
                return NotFound();
            }

            _logger.LogInformation("Request successful");
            return Ok(congressMembers);
        }

        [HttpDelete("{id}")]
        [ProducesResponseType(typeof(CongressMember), StatusCodes.Status200OK)]
        public async ValueTask<IActionResult> DeleteAsync(string id)
        {
            _logger.LogInformation($"[DELETE Request] id = {id}");

            CongressMember? congressMember = null;
            try
            {
                congressMember = await _congressMemberService.DeleteCongressMemberAsync(id);
            }
            catch (Exception e)
            {
                _logger.LogWarning(e.ToString());
                return StatusCode(StatusCodes.Status500InternalServerError, e.ToString());
            }

            if (congressMember is null)
            {
                return NotFound();
            }

            _logger.LogInformation($"Request successful, returning: {JsonConvert.SerializeObject(congressMember)}");
            return Ok(congressMember);
        }
    }
}