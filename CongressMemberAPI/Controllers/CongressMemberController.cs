using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Newtonsoft.Json;
using Common.Models;
using Common.Services;

namespace CongressMemberAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class CongressMemberController : ControllerBase
    {
        private readonly ILogger<CongressMemberController> _logger;
        private readonly ICongressMemberService _congressMemberService;

        public CongressMemberController(
            ILogger<CongressMemberController> logger,
            ICongressMemberService congressMemberService)
        {
            _logger = logger;
            _congressMemberService = congressMemberService;
        }

        [HttpPost]
        [ProducesResponseType(typeof(CongressMember), StatusCodes.Status201Created)]
        public async ValueTask<IActionResult> CreateOrUpdateAsync(CongressMember congressMember)
        {
            _logger.LogInformation($"[POST Request] {JsonConvert.SerializeObject(congressMember)}");

            var modifiedCongressMember = new CongressMember();
            try
            {
                modifiedCongressMember = await _congressMemberService.CreateOrUpdateCongressMemberAsync(congressMember);
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

            if (modifiedCongressMember is null)
            {
                var error = "[ERROR] Congress Member object returned is null";
                _logger.LogError(error);
                return StatusCode(StatusCodes.Status500InternalServerError, error);
            }

            _logger.LogInformation($"Request successful, returning: {JsonConvert.SerializeObject(modifiedCongressMember)}");
            return CreatedAtAction(nameof(GetAsync), new { id = modifiedCongressMember.ID }, modifiedCongressMember);
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