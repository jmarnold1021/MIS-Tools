DROP TABLE [dbo].[L56_DOD_SCFF]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[L56_DOD_SCFF]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[L56_DOD_SCFF](
	[GI03] [varchar](3) NOT NULL,
	[SB00] [varchar](9) NOT NULL,
	[CCPG] [varchar](1) NULL,
	[PELL] [varchar](1) NULL,
	[ADT] [varchar](1) NULL,
	[ADT_CCPG] [varchar](1) NULL,
	[ADT_PELL] [varchar](1) NULL,
	[AAAS] [varchar](1) NULL,
	[AAAS_CCPG] [varchar](1) NULL,
	[AAAS_PELL] [varchar](1) NULL,
	[BABS] [varchar](1) NULL,
	[BABS_CCPG] [varchar](1) NULL,
	[BABS_PELL] [varchar](1) NULL,
	[CERT] [varchar](1) NULL,
	[CERT_CCPG] [varchar](1) NULL,
	[CERT_PELL] [varchar](1) NULL,
	[XFERLEVEL] [varchar](1) NULL,
	[XFERLEVEL_CCPG] [varchar](1) NULL,
	[XFERLEVEL_PELL] [varchar](1) NULL,
	[CTE] [varchar](1) NULL,
	[CTE_CCPG] [varchar](1) NULL,
	[CTE_PELL] [varchar](1) NULL,
	[XFER] [varchar](1) NULL,
	[XFER_CCPG] [varchar](1) NULL,
	[XFER_PELL] [varchar](1) NULL,
	[WAGE] [varchar](1) NULL,
	[WAGE_CCPG] [varchar](1) NULL,
	[WAGE_PELL] [varchar](1) NULL,
 CONSTRAINT [PK_DOD_SCFF_GI03_SB00] PRIMARY KEY CLUSTERED 
(
	[GI03] DESC,
	[SB00] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
END
GO
