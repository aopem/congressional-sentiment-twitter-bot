namespace Common.Brokers
{
    public class DatabaseBroker
    {
        public DatabaseBroker()
        {
        }

        public async ValueTask<T> InsertAsync<T>(T data)
        {
            await return;
        }

        public async ValueTask<T> UpdateAsync<T>(T data)
        {
            await return;
        }

        public async ValueTask<T> SelectByIdAsync<T>(Guid id)
        {
            await return;
        }

        public IQueryable<T> SelectAllAsync<T>()
        {
            return;
        }

        public async ValueTask<T> DeleteByIdAsync<T>(Guid id)
        {
            await return;
        }
    }
}