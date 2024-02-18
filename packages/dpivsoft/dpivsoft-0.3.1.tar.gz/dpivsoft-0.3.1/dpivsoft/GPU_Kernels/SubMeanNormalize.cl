KERNEL void SubMeanNormalize(GLOBAL_MEM float2 *subImg,
                              GLOBAL_MEM int *data)
{
    int box_size_x = data[2];
    int box_size_y = data[3];
    float mean = 0.0;
    int count = 0;

    const SIZE_T i = get_global_id(0);
    int pos = i / (box_size_x * box_size_y);

    // Compute mean within the box
    for (int j = 0; j < box_size_y; j++)
    {
        for (int k = 0; k < box_size_x; k++)
        {
            int idx = pos * box_size_y * box_size_x + box_size_x * j + k;
            // Add only non-masked values
            if (subImg[idx].x)
            {
                mean += subImg[idx].x;
                count++;
            }
        }
    }

    // Compute the mean
    mean /= count;

    // Normalize within the box
    if (subImg[i].x)
    {
        subImg[i].x -= mean;
    }
}