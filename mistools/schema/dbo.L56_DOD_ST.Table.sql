DROP TABLE [dbo].[L56_DOD_ST]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[L56_DOD_ST]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[L56_DOD_ST](
	[GI01] [varchar](3) NULL,
	[CCCCO_Assigned] [varchar](9) NOT NULL,
	[GI03] [varchar](3) NOT NULL,
	[STD1] [int] NULL,
	[SB08] [varchar](5) NULL,
	[SB08B] [varchar](4) NULL,
	[SB09] [varchar](5) NULL,
	[SB11] [varchar](5) NULL,
	[SB12] [varchar](12) NULL,
	[SB15] [varchar](1) NULL,
	[SB16] [decimal](6, 2) NULL,
	[SB17] [decimal](6, 2) NULL,
	[SB18] [decimal](6, 2) NULL,
	[SB19] [decimal](6, 2) NULL,
	[SB20] [decimal](6, 2) NULL,
	[SB21] [decimal](6, 2) NULL,
	[STD8] [decimal](3, 2) NULL,
	[STD9] [decimal](3, 2) NULL,
	[SB22] [varchar](1) NULL,
	[SB23] [varchar](1) NULL,
	[SB24] [varchar](1) NULL,
	[SB25] [varchar](1) NULL,
	[SB14] [varchar](1) NULL,
	[SB31] [varchar](30) NULL,
	[SB32] [varchar](30) NULL,
	[SB04] [varchar](1) NULL,
	[SB06] [varchar](1) NULL,
	[SB26] [varchar](1) NULL,
	[STD2] [decimal](4, 2) NULL,
	[STD3] [varchar](1) NULL,
	[STD6] [varchar](1) NULL,
	[STD4] [varchar](1) NULL,
	[STD5] [decimal](4, 2) NULL,
	[STD7] [varchar](1) NULL,
	[SB27] [varchar](1) NULL,
	[SB29] [varchar](21) NULL,
	[STD10] [varchar](1) NULL,
	[SB30] [varchar](1) NULL,
	[SB33] [varchar](2) NULL,
	[SB36] [varchar](1) NULL,
	[SB37] [varchar](1) NULL,
	[SB38] [varchar](194) NULL,
	[SB39] [varchar](2) NULL,
 CONSTRAINT [PK_DOD_ST_GI03_CCCCO_Assigned] PRIMARY KEY CLUSTERED 
(
	[GI03] DESC,
	[CCCCO_Assigned] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
END
GO
